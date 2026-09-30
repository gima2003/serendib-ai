from typing import TypedDict, List, Dict, Any, Optional

class ScheduleState(TypedDict):
    trip_id: str
    
    # Inputs
    profile: Dict[str, Any]
    destinations: List[Dict[str, Any]]
    stays: List[Dict[str, Any]]
    food_options: List[Dict[str, Any]]
    route_plan: Dict[str, Any]
    budget_plan: Dict[str, Any]
    safety_plan: Dict[str, Any]
    context_plan: Dict[str, Any]
    
    # Intermediary variables
    current_day: int
    allocated_days: Dict[str, int]
    
    # Outputs
    itinerary: List[Dict[str, Any]]
    warnings: List[str]
    notes: List[str]
    is_valid: bool
