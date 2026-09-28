import logging
from agents.planner.schedule.schemas import ScheduleAgentRequest, ScheduleResponse
from agents.planner.schedule.schedule_builder import build_itinerary

logger = logging.getLogger(__name__)

async def generate_schedule(request: ScheduleAgentRequest) -> ScheduleResponse:
    """
    Main entry point for the Schedule Agent.
    Orchestrates building the chronological itinerary and validating it.
    """
    logger.info(f"Starting Schedule compilation for trip")
    
    # Compile itinerary
    response = build_itinerary(request)
    
    # Optional: Run validation checks (e.g. impossible travel times)
    conflicts = validate_schedule(response)
    if conflicts:
        response.overall_warnings.extend(conflicts)
        
    logger.info("Schedule compilation finished successfully.")
    return response

def validate_schedule(response: ScheduleResponse) -> list[str]:
    conflicts = []
    
    # 1. Missing accommodation for overnight stay
    for day in response.itinerary:
        if not day.accommodation:
            conflicts.append(f"Day {day.day} in {day.city} is missing a selected accommodation.")
            
    # 2. Activity count warning
    for day in response.itinerary:
        if len(day.activities) > 8:
            conflicts.append(f"Day {day.day} has {len(day.activities)} scheduled activities which might be too packed.")
            
    return conflicts
