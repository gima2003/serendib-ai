import logging
from typing import Dict, Any

from state import TripState
from agents.planner.context.context_orchestrator import context_plan

logger = logging.getLogger(__name__)

async def process_context(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node — Agent 4 (Context: Weather, Crowd, Alerts).
    Reads 'profile', 'destinations', and 'route_plan'.
    Updates 'context_plan'.
    """
    logger.info("Executing Context Node")
    
    profile = state.get("profile")
    destinations = state.get("destinations", [])
    route_plan = state.get("route_plan")
    
    if not profile or not route_plan:
        logger.warning("Missing required state for context (profile or route_plan).")
        return {}
        
    try:
        profile_dict = profile.model_dump()
        
        # Build destinations list with all key variants so orchestrator can find them
        destinations_list = []
        for d in destinations:
            city_name = d.get("city") or d.get("destination")
            if city_name:
                destinations_list.append({
                    "destination": city_name,
                    "city": city_name,
                    "location": city_name,  # FIX: was using "location" key that was missing
                    "category": d.get("category", ""),
                })
        
        # Serialize route with normalized leg keys for coord lookup
        route_dict = route_plan.model_dump()
        normalized_legs = []
        for leg in route_dict.get("legs", []):
            coords = leg.get("coordinates", {})
            normalized_legs.append({
                **leg,
                "from_location": leg.get("from_location", ""),
                "to_location": leg.get("to_location", ""),
                "coordinates": {
                    "origin": coords.get("origin") if isinstance(coords.get("origin"), dict) else {},
                    "destination": coords.get("destination") if isinstance(coords.get("destination"), dict) else {},
                }
            })
        route_dict["legs"] = normalized_legs
        
        context_resp = await context_plan(
            profile_dict,
            destinations_list,
            route_dict
        )
        
        logger.info(f"Context: {len(context_resp.weather_predictions)} weather predictions, {len(context_resp.crowd_predictions)} crowd predictions")
        return {"context_plan": context_resp}
    except Exception as e:
        logger.error(f"Error in Context Node: {str(e)}", exc_info=True)
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Context planning failed: {str(e)}"]}
