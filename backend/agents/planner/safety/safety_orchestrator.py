from typing import Dict, Any, List, Tuple
from .schemas import SafetyResponse
from .landslide_hazard_service import check_hazard_level
from .incident_analysis_service import check_nearby_incidents
from .weather_service import get_weather_forecast
from .route_safety_service import calculate_safety_score
from .trip_replanning_service import check_replanning

def _interpolate_points(start_lat: float, start_lon: float, end_lat: float, end_lon: float, num_points: int = 5) -> List[Tuple[float, float]]:
    points = []
    if num_points <= 1:
        return [(start_lat, start_lon)]
        
    for i in range(num_points):
        fraction = i / (num_points - 1)
        lat = start_lat + (end_lat - start_lat) * fraction
        lon = start_lon + (end_lon - start_lon) * fraction
        points.append((lat, lon))
    return points

async def safety_plan(profile: Dict[str, Any], destinations: List[Dict[str, Any]], route_response: Dict[str, Any]) -> SafetyResponse:
    # --- DESTINATION SAFETY CHECK (Existing) ---
    dest_lat = 0.0
    dest_lon = 0.0
    
    if route_response and route_response.get("coordinates") and len(route_response["coordinates"]) > 0:
        coord = route_response["coordinates"][-1] # use last as destination
        dest_lat = coord.get("lat", 0.0)
        dest_lon = coord.get("lon", 0.0)
    elif destinations and len(destinations) > 0:
        dest_lat = destinations[-1].get("latitude", 0.0)
        dest_lon = destinations[-1].get("longitude", 0.0)
        
    travel_date = profile.get("travel_date", "2024-01-01")
    activities = profile.get("activities", [])
    
    dest_hazard_info = check_hazard_level(dest_lat, dest_lon)
    dest_incident_info = check_nearby_incidents(dest_lat, dest_lon)
    dest_weather_info = get_weather_forecast(dest_lat, dest_lon, travel_date)
    
    # --- ROUTE SEGMENT SAFETY ANALYSIS (New) ---
    route_segments = []
    legs = route_response.get("legs", []) if route_response else []
    
    total_segment_score = 0
    segment_explanations = []
    max_hazard_range = dest_hazard_info["hazard_range"]
    total_incidents = dest_incident_info["nearby_incidents"]
    
    for leg in legs:
        start_name = leg.get("from", "Unknown")
        end_name = leg.get("to", "Unknown")
        start_loc = leg.get("start_location", {})
        end_loc = leg.get("end_location", {})
        
        start_lat = start_loc.get("lat", 0.0)
        start_lon = start_loc.get("lon", 0.0)
        end_lat = end_loc.get("lat", 0.0)
        end_lon = end_loc.get("lon", 0.0)
        
        # Check multiple points along the route leg
        points = _interpolate_points(start_lat, start_lon, end_lat, end_lon, 5)
        
        leg_max_hazard = 1
        leg_max_incidents = 0
        leg_weather = dest_weather_info # default to destination weather if api fails or to save calls
        
        # Evaluate points
        for (p_lat, p_lon) in points:
            h_info = check_hazard_level(p_lat, p_lon)
            i_info = check_nearby_incidents(p_lat, p_lon)
            
            if h_info["hazard_range"] > leg_max_hazard:
                leg_max_hazard = h_info["hazard_range"]
            if i_info["nearby_incidents"] > leg_max_incidents:
                leg_max_incidents = i_info["nearby_incidents"]
                
        # Get weather for the end of the leg
        leg_weather = get_weather_forecast(end_lat, end_lon, travel_date)
        
        leg_safety_eval = calculate_safety_score(
            hazard_range=leg_max_hazard,
            rain_prob=leg_weather["rain_probability"],
            weather_cond=leg_weather["weather_condition"],
            incidents=leg_max_incidents
        )
        
        route_segments.append({
            "from": start_name,
            "to": end_name,
            "safety_score": leg_safety_eval["safety_score"],
            "risk_level": leg_safety_eval["risk_level"]
        })
        
        total_segment_score += leg_safety_eval["safety_score"]
        
        # Track max hazard and total incidents for explanation
        if leg_max_hazard > max_hazard_range:
            max_hazard_range = leg_max_hazard
        total_incidents += leg_max_incidents
        
        if leg_max_hazard >= 3:
            segment_explanations.append(f"LHMP Hazard Range {leg_max_hazard} detected on route {start_name} to {end_name}")
        if leg_max_incidents > 0:
            segment_explanations.append(f"{leg_max_incidents} historical landslide incidents found near route {start_name} to {end_name}")
            
    # Calculate final safety score
    if len(route_segments) > 0:
        final_safety_score = int(total_segment_score / len(route_segments))
    else:
        # Fallback to destination-only score if no legs
        dest_safety_eval = calculate_safety_score(
            hazard_range=dest_hazard_info["hazard_range"],
            rain_prob=dest_weather_info["rain_probability"],
            weather_cond=dest_weather_info["weather_condition"],
            incidents=dest_incident_info["nearby_incidents"]
        )
        final_safety_score = dest_safety_eval["safety_score"]
        
    # Re-evaluate final risk level based on final score
    if final_safety_score >= 80:
        final_risk_level = "LOW"
    elif final_safety_score >= 50:
        final_risk_level = "MEDIUM"
    else:
        final_risk_level = "HIGH"

    # --- SAFETY EXPLANATION (New) ---
    safety_explanation = []
    
    # Hazard explanation
    if max_hazard_range >= 3:
        safety_explanation.append(f"LHMP Hazard Range {max_hazard_range} detected near route")
        
    # Incident explanation
    if total_incidents > 0:
        safety_explanation.append(f"{total_incidents} historical landslide incidents found within 5km of the route")
        
    # Weather explanation
    # Check overall weather condition (e.g. at destination or worst leg weather)
    # We will use the destination weather or check if heavy rain was found
    is_heavy_rain = ("heavy" in dest_weather_info["weather_condition"] or dest_weather_info["rain_probability"] > 80)
    is_rain = ("rain" in dest_weather_info["weather_condition"] or dest_weather_info["rain_probability"] > 50)
    
    if is_heavy_rain:
        safety_explanation.append("Heavy rainfall forecast during travel date")
    elif is_rain:
        safety_explanation.append("Rainfall forecast during travel date")
        
    # Also add the leg-specific explanations (deduplicated or keep them separate)
    # For a clean explanation list, we can just use the global ones as requested in the example.
    # But if there's no overall hazard, let's keep it simple.
    
    # 4. Check replanning
    replan_eval = check_replanning(
        risk_level=final_risk_level,
        weather_condition=dest_weather_info["weather_condition"],
        activities=activities
    )
    
    # 5. Generate warnings
    warnings = []
    if final_risk_level == "HIGH":
        warnings.append("High safety risk detected for the planned route.")
    if max_hazard_range >= 3:
        warnings.append(f"Location or route is in a hazard zone (Range {max_hazard_range}).")
        
    # 6. Return response
    return SafetyResponse(
        trip_id=profile.get("trip_id", "TRIP-001"),
        route_safety_score=final_safety_score,
        risk_level=final_risk_level,
        route_segments=route_segments,
        safety_explanation=safety_explanation,
        weather_summary=dest_weather_info,
        hazard_summary=dest_hazard_info,
        incident_summary=dest_incident_info,
        warnings=warnings,
        recommendations=replan_eval["suggestions"],
        replanning_required=replan_eval["replanning_required"],
        replanning_actions=replan_eval["suggestions"],
        data_sources=["LHMP_50000", "Historical Incidents", "OpenWeather"]
    )
