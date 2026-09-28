import logging
from typing import Dict, Any

from state import TripState
from agents.planner.route.schemas import RouteRequest
from agents.planner.route.route_orchestrator import route_plan

logger = logging.getLogger(__name__)

async def process_route(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node — Agent 4 (Route).
    Reads 'profile' and 'destinations' from state and updates 'route_plan'.
    Route is built using: starting_location → must_visit destinations → AI destinations.
    """
    logger.info("Executing Route Node")
    
    profile = state.get("profile")
    destinations = state.get("destinations", [])
    
    if not profile or not destinations:
        logger.warning("Missing profile or destinations, skipping route planning.")
        return {}
        
    try:
        # Build the route sequentially: start → destinations (already ordered by priority in dest node)
        route_destinations = []
        if profile.starting_location:
            route_destinations.append(profile.starting_location)
            
        seen = set()
        if profile.starting_location:
            seen.add(profile.starting_location.lower().strip())
            
        for d in destinations:
            city_name = d.get("city") or d.get("destination")
            if city_name:
                norm = city_name.lower().strip()
                if norm not in seen:
                    route_destinations.append(city_name)
                    seen.add(norm)
        
        if len(route_destinations) < 2:
            logger.warning(f"Not enough destinations for route: {route_destinations}")
            return {}
        
        # Map travel pace to travel style
        travel_style = "moderate"
        if profile.travel_pace:
            travel_style = profile.travel_pace.value
        
        # Determine transport preferences
        from models.traveller_profile import TravelType
        transport_prefs = ["car"]  # Default for comfort
        if profile.travel_type == TravelType.family:
            transport_prefs = ["car"]  # Family always prefers car for flexibility
        
        route_req = RouteRequest(
            trip_id=state.get("trip_id", "default_trip"),
            destinations=route_destinations,
            travel_style=travel_style,
            transport_preferences=transport_prefs,
            budget_level="moderate"
        )
        
        logger.info(f"Route request: {route_destinations}")
        route_resp = await route_plan(route_req)
        logger.info(f"Route complete: {route_resp.route_summary.total_distance_km:.0f} km, {route_resp.route_summary.total_estimated_duration_minutes:.0f} min")
        
        return {"route_plan": route_resp}
    except Exception as e:
        logger.error(f"Error in Route Node: {str(e)}", exc_info=True)
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Route planning failed: {str(e)}"]}
