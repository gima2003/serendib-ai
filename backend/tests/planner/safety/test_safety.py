import pytest
from backend.agents.planner.safety.landslide_hazard_service import check_hazard_level
from backend.agents.planner.safety.incident_analysis_service import check_nearby_incidents
from backend.agents.planner.safety.weather_service import get_weather_forecast, _fallback_weather
from backend.agents.planner.safety.route_safety_service import calculate_safety_score
from backend.agents.planner.safety.trip_replanning_service import check_replanning

def test_hazard_range_mapping():
    # Will gracefully return a valid hazard range even if coordinates don't intersect
    res = check_hazard_level(0.0, 0.0)
    assert "hazard_range" in res
    assert res["hazard_range"] in [1, 2, 3, 4]
    assert res["risk_level"] in ["LOW", "MODERATE", "HIGH", "VERY_HIGH"]

def test_incident_radius_search():
    res = check_nearby_incidents(0.0, 0.0)
    assert "nearby_incidents" in res
    assert isinstance(res["nearby_incidents"], int)

def test_weather_api_failure():
    # Calling without mock or API KEY should return fallback
    res = get_weather_forecast(0.0, 0.0, "2024-01-01")
    assert res == _fallback_weather()

def test_safety_score_calculation():
    # Scenario: High Risk
    res = calculate_safety_score(hazard_range=4, rain_prob=90, weather_cond="heavy rain", incidents=2)
    assert res["safety_score"] == 35  # 100 - 30 (range 4) - 25 (heavy rain) - 10 (2*5 incidents)
    assert res["risk_level"] == "HIGH"
    
    # Scenario: Low Risk
    res2 = calculate_safety_score(hazard_range=1, rain_prob=10, weather_cond="clear", incidents=0)
    assert res2["safety_score"] == 100
    assert res2["risk_level"] == "LOW"

def test_dynamic_replanning_trigger():
    res = check_replanning("HIGH", "heavy rain", ["Outdoor hiking"])
    assert res["replanning_required"] is True
    assert "Select safer attractions" in res["suggestions"]
    assert "Move outdoor attractions to another day" in res["suggestions"]
    assert "Delay hiking activities" in res["suggestions"]
    assert "Travel during daytime" in res["suggestions"]

def test_safety_orchestrator():
    import asyncio
    from backend.agents.planner.safety.safety_orchestrator import safety_plan
    profile = {"trip_id": "TEST", "travel_date": "2024-01-01", "activities": ["Sightseeing"]}
    destinations = [{"latitude": 6.8, "longitude": 81.0}]
    route_response = {
        "coordinates": [{"lat": 6.8, "lon": 81.0}],
        "legs": [
            {
                "from": "Colombo",
                "to": "Kandy",
                "start_location": {"lat": 6.9, "lon": 79.8},
                "end_location": {"lat": 7.2, "lon": 80.6}
            },
            {
                "from": "Kandy",
                "to": "Ella",
                "start_location": {"lat": 7.2, "lon": 80.6},
                "end_location": {"lat": 6.8, "lon": 81.0}
            }
        ]
    }
    
    response = asyncio.run(safety_plan(profile, destinations, route_response))
    
    assert response.route_safety_score >= 0
    assert response.risk_level in ["LOW", "MEDIUM", "HIGH"]
    assert len(response.route_segments) == 2
    assert response.route_segments[0]["from"] == "Colombo"
    assert response.route_segments[1]["from"] == "Kandy"
    assert "safety_score" in response.route_segments[0]
    
    # Test explanation generation
    assert isinstance(response.safety_explanation, list)
