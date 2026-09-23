import pytest
import asyncio
from backend.agents.planner.context.context_orchestrator import context_plan
from backend.agents.planner.context.weather_context_service import get_weather_prediction
from backend.agents.planner.context.crowd_prediction_service import calculate_crowd_prediction, is_long_weekend

def test_context_orchestration():
    profile = {
        "trip_id": "TEST-1",
        "start_date": "2026-09-26",
        "end_date": "2026-09-26"
    }
    destinations = [
        {"location": "Ella", "category": "popular", "latitude": 6.8667, "longitude": 81.0466}
    ]
    
    response = asyncio.run(context_plan(profile, destinations, {}))
    
    assert response.trip_id == "TEST-1"
    assert len(response.crowd_predictions) == 1
    assert len(response.weather_predictions) == 1
    
    # 2026-09-26 is a Poya day and Ella is popular, so it should generate a crowd alert
    crowd_alerts = [a for a in response.context_alerts if a.type == "crowd"]
    assert len(crowd_alerts) > 0
    assert "Full Moon Poya Day" in crowd_alerts[0].message
    
    # Ella has a mock rain probability of 80%, so it should generate a weather alert
    weather_alerts = [a for a in response.context_alerts if a.type == "weather"]
    assert len(weather_alerts) > 0
    assert "Rain may affect hiking activities" in weather_alerts[0].message

def test_holiday_detection():
    # 2026-09-26 is in the mock calendar as Poya day
    assert is_long_weekend("2026-09-26") is False # Saturday Poya without Monday holiday
    # 2026-05-01 is May Day (Friday) -> Long weekend
    assert is_long_weekend("2026-05-01") is True

def test_crowd_prediction():
    prediction = calculate_crowd_prediction("2026-09-26", "Ella")
    assert prediction.crowd_level in ["HIGH", "VERY_HIGH"]
    assert "Full Moon Poya Day" in prediction.reasons

def test_weather_api_failure_handling(monkeypatch):
    # Force API key to exist so it attempts network call
    monkeypatch.setattr("backend.agents.planner.context.weather_context_service.OPENWEATHER_API_KEY", "invalid_key_for_test")
    
    # It should fail gracefully and fall back to the mock data for Ella
    weather = asyncio.run(get_weather_prediction("Ella", 0.0, 0.0, "2026-09-24"))
    
    assert weather.location == "Ella"
    assert weather.rain_probability == 80
    assert weather.weather_condition == "Heavy Rain"
    assert "Move hiking activities to morning" in weather.recommendations

def test_recommendation_generation():
    profile = {
        "trip_id": "TEST-1",
        "start_date": "2026-09-26",
        "end_date": "2026-09-26"
    }
    destinations = [
        {"location": "Ella", "category": "popular"}
    ]
    
    response = asyncio.run(context_plan(profile, destinations, {}))
    
    assert len(response.recommendations) > 0
    
    # Check that recommendations from both crowd (HIGH) and weather (Rain) are aggregated
    assert "Visit popular attractions early morning" in response.recommendations
    assert "Consider indoor alternatives" in response.recommendations

