from typing import TypedDict, List, Dict, Any, Optional
from models.traveller_profile import TravellerProfile
from agents.accommodation.schemas import AccommodationResponse, DestinationAccommodation
from agents.planner.route.schemas import RouteResponse
from agents.planner.budget.schemas import BudgetResponse
from agents.planner.safety.schemas import SafetyResponse
from agents.planner.context.schemas import ContextResponse
from agents.planner.schedule.schemas import ScheduleResponse

class TripState(TypedDict):
    """
    Shared LangGraph state for the Serendib AI trip planning pipeline.
    Preserves all agent outputs and avoids business logic.
    """
    # 1. Pipeline Status & Metadata
    trip_id: str
    status: str
    errors: List[str]
    warnings: List[str]
    
    # Loop Protection & Decision History
    budget_replan_attempts: int
    safety_replan_attempts: int
    context_replan_attempts: int
    decision_history: List[Dict[str, Any]]
    
    # 2. User Input
    raw_user_request: str
    
    # 3. Agent 1: Profile Extraction
    profile: Optional[TravellerProfile]
    
    # 4. Agent 2: Destination & Experience
    # List of dictionaries, each containing city, attractions, scores.
    # We use Dict here because Agent 2 currently returns unstructured dicts in integration_test.py
    destinations: List[Dict[str, Any]]
    
    # 5. Agent 3: Food & Accommodation
    # List of dictionaries for food options
    food_options: List[Dict[str, Any]]
    
    # Strict Pydantic-backed accommodation structure
    accommodation_plan: Optional[AccommodationResponse]
    # For easier access to just the stays if needed
    stays: List[DestinationAccommodation]
    
    # 6. Agent 4: Planners (Route, Budget, Safety, Context)
    route_plan: Optional[RouteResponse]
    budget_plan: Optional[BudgetResponse]
    safety_plan: Optional[SafetyResponse]
    context_plan: Optional[ContextResponse]
    
    # 7. Agent 5: Final Schedule
    schedule_plan: Optional[ScheduleResponse]
