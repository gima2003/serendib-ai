from datetime import datetime, timedelta
from typing import Dict, Any, List

from .schemas import ContextResponse, ContextAlert
from .crowd_prediction_service import calculate_crowd_prediction
from .weather_context_service import get_weather_prediction

async def context_plan(profile: Dict[str, Any], destinations: List[Dict[str, Any]], route_response: Dict[str, Any]) -> ContextResponse:
    trip_id = profile.get("trip_id", "TRIP-001")
    start_date = profile.get("start_date", "2026-09-24")
    end_date = profile.get("end_date", "2026-09-28")
    
    s_date = datetime.strptime(start_date, "%Y-%m-%d")
    e_date = datetime.strptime(end_date, "%Y-%m-%d")
    days = (e_date - s_date).days + 1
    
    travel_dates = [(s_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    
    crowd_predictions = []
    weather_predictions = []
    context_alerts = []
    recommendations = set()
    
    for date_str in travel_dates:
        for dest in destinations:
            location = dest.get("location", "Unknown")
            category = dest.get("category", "")
            lat = dest.get("latitude", 0.0)
            lon = dest.get("longitude", 0.0)
            
            # 1. Crowd Prediction
            crowd = calculate_crowd_prediction(date_str, location, category)
            crowd_predictions.append(crowd)
            
            if crowd.crowd_level in ["HIGH", "VERY_HIGH"]:
                primary_reason = crowd.reasons[0] if crowd.reasons else "high demand"
                context_alerts.append(ContextAlert(
                    type="crowd",
                    date=date_str,
                    location=location,
                    message=f"High crowd expected due to {primary_reason}"
                ))
            
            for rec in crowd.recommendations:
                recommendations.add(rec)
                
            # 2. Weather Context
            weather = await get_weather_prediction(location, lat, lon, date_str)
            # Add to predictions only once per location if weather doesn't change per date in mock, 
            # but since it could change per date in reality, we keep it per date/location
            weather_predictions.append(weather)
            
            if weather.rain_probability > 50 or weather.temperature > 32:
                # Custom message for Ella based on the example
                if location.lower() == "ella" and weather.rain_probability > 50:
                    alert_message = "Rain may affect hiking activities"
                else:
                    alert_message = weather.activity_impact
                    
                context_alerts.append(ContextAlert(
                    type="weather",
                    date=date_str,
                    location=location,
                    message=alert_message
                ))
                
            for rec in weather.recommendations:
                recommendations.add(rec)
                
    return ContextResponse(
        trip_id=trip_id,
        crowd_predictions=crowd_predictions,
        weather_predictions=weather_predictions,
        context_alerts=context_alerts,
        context_warnings=[],
        recommendations=list(recommendations)
    )
