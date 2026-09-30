from datetime import datetime, timedelta
from typing import Dict, Any, List

from .schemas import ContextResponse, ContextAlert
from .crowd_prediction_service import calculate_crowd_prediction
from .weather_context_service import get_weather_prediction

async def context_plan(profile: Dict[str, Any], destinations: List[Dict[str, Any]], route_response: Dict[str, Any]) -> ContextResponse:
    trip_id = profile.get("trip_id", "TRIP-001")
    
    # Try to extract start_date from profile; fall back to today's date
    start_date_raw = profile.get("start_date") or profile.get("travel_date")
    if not start_date_raw:
        start_date_raw = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Parse start_date safely
    try:
        s_date = datetime.strptime(start_date_raw[:10], "%Y-%m-%d")
    except (ValueError, TypeError):
        s_date = datetime.utcnow()
    
    duration_days = profile.get("duration_days") or 5
    e_date = s_date + timedelta(days=int(duration_days) - 1)
    days = max(1, (e_date - s_date).days + 1)
    
    travel_dates = [(s_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    
    crowd_predictions = []
    weather_predictions = []
    context_alerts = []
    recommendations = set()
    
    # Build a location → coord map from route_response legs
    coord_map: Dict[str, Dict] = {}
    for leg in route_response.get("legs", []):
        coords = leg.get("coordinates", {})
        if leg.get("from_location") and coords.get("origin"):
            coord_map[leg["from_location"].lower()] = coords["origin"]
        if leg.get("to_location") and coords.get("destination"):
            coord_map[leg["to_location"].lower()] = coords["destination"]
    
    # De-duplicate: only one weather+crowd prediction per unique location
    seen_locations = set()
    
    for dest in destinations:
        # FIX: accept both "location" and "destination" keys
        location = (
            dest.get("location") 
            or dest.get("destination") 
            or dest.get("city") 
            or "Unknown"
        )
        if not location or location == "Unknown":
            continue
            
        category = dest.get("category", "")
        
        # Lookup coordinates from route legs if available
        loc_key = location.lower()
        coord = coord_map.get(loc_key, {})
        lat = coord.get("lat", 0.0)
        lon = coord.get("lon", 0.0)
        
        # Only predict for each unique location once to avoid duplicates
        if loc_key in seen_locations:
            continue
        seen_locations.add(loc_key)
        
        # Use the travel date that best matches this location's position in the trip
        date_str = travel_dates[min(len(seen_locations) - 1, len(travel_dates) - 1)]
        
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
        weather_predictions.append(weather)
        
        if weather.rain_probability > 50 or weather.temperature > 32:
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
