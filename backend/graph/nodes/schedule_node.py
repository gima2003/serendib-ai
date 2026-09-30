import logging
from typing import Dict, Any

from state import TripState
from agents.planner.schedule.schedule_service import generate_schedule
from agents.planner.schedule.schemas import ScheduleAgentRequest

logger = logging.getLogger(__name__)

async def process_schedule(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node that acts as a thin wrapper around Agent 5 (Schedule).
    Reads all available specialist plans from state.
    Updates 'schedule_plan'.
    """
    logger.info("Executing Schedule Node")
    
    profile = state.get("profile")
    destinations = state.get("destinations", [])
    food_options = state.get("food_options", [])
    accommodation_plan = state.get("accommodation_plan")
    route_plan = state.get("route_plan")
    budget_plan = state.get("budget_plan")
    safety_plan = state.get("safety_plan")
    context_plan = state.get("context_plan")
    
    if not profile or not route_plan or not accommodation_plan:
        logger.warning("Missing required state for schedule. Need at least profile, route, and accommodation.")
        return {}
        
    try:
        schedule_req = ScheduleAgentRequest(
            profile=profile,
            destinations=destinations,
            stays=accommodation_plan.accommodation_plan,
            food_options=food_options,
            route_plan=route_plan,
            budget_plan=budget_plan,
            safety_plan=safety_plan,
            context_plan=context_plan
        )
        
        schedule_resp = await generate_schedule(schedule_req)
        
        return {"schedule_plan": schedule_resp}
    except Exception as e:
        logger.error(f"Error in Schedule Node: {str(e)}")
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Schedule generation failed: {str(e)}"]}
