import logging
from typing import Dict, Any

from state import TripState
from agents.planner.safety.safety_orchestrator import safety_plan

logger = logging.getLogger(__name__)

async def process_safety(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node — Agent 4 (Safety).
    Reads 'profile', 'destinations', and 'route_plan'.
    Updates 'safety_plan'.
    """
    logger.info("Executing Safety Node")
    
    profile = state.get("profile")
    destinations = state.get("destinations", [])
    route_plan = state.get("route_plan")
    
    if not profile or not route_plan:
        logger.warning("Missing required state for safety (profile or route_plan).")
        return {}
        
    try:
        profile_dict = profile.model_dump()
        
        # Pass destinations with both 'destination' and 'city' keys for compatibility
        destinations_list = []
        for d in destinations:
            city_name = d.get("city") or d.get("destination")
            if city_name:
                destinations_list.append({
                    "destination": city_name,
                    "city": city_name,
                    "location": city_name  # Also pass as "location" for any consumers expecting that key
                })
        
        # Serialize route_plan as dict; safety orchestrator reads "legs" 
        route_dict = route_plan.model_dump()
        
        # Normalize leg keys: safety orchestrator reads "from"/"to" keys
        # but route_plan uses "from_location"/"to_location"
        normalized_legs = []
        for leg in route_dict.get("legs", []):
            coords = leg.get("coordinates", {})
            origin_coord = coords.get("origin", {})
            dest_coord = coords.get("destination", {})
            
            # Convert Coordinate objects to plain dicts with lat/lon
            if hasattr(origin_coord, "lat"):
                origin_coord = {"lat": origin_coord.lat, "lon": origin_coord.lon}
            if hasattr(dest_coord, "lat"):
                dest_coord = {"lat": dest_coord.lat, "lon": dest_coord.lon}
            
            normalized_legs.append({
                "from": leg.get("from_location", "Unknown"),
                "to": leg.get("to_location", "Unknown"),
                "from_location": leg.get("from_location", "Unknown"),
                "to_location": leg.get("to_location", "Unknown"),
                "start_location": origin_coord if isinstance(origin_coord, dict) else {},
                "end_location": dest_coord if isinstance(dest_coord, dict) else {},
            })
        
        route_dict["legs"] = normalized_legs
                
        safety_resp = await safety_plan(
            profile_dict,
            destinations_list,
            route_dict
        )
        
        logger.info(f"Safety: risk_level={safety_resp.risk_level}, score={safety_resp.route_safety_score}")
        return {"safety_plan": safety_resp}
    except Exception as e:
        logger.error(f"Error in Safety Node: {str(e)}", exc_info=True)
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Safety planning failed: {str(e)}"]}
