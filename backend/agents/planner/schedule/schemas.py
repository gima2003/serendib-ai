from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from models.traveller_profile import TravellerProfile
from agents.accommodation.schemas import DestinationAccommodation
from agents.planner.budget.schemas import FoodRecommendation, BudgetResponse
from agents.planner.route.schemas import RouteResponse
from agents.planner.safety.schemas import SafetyResponse
from agents.planner.context.schemas import ContextResponse

class ScheduleAgentRequest(BaseModel):
    profile: TravellerProfile
    destinations: List[Dict[str, Any]]  # Output from Agent 2
    stays: List[DestinationAccommodation]
    food_options: List[Dict[str, Any]] # Output from Agent 3 Food (since food agent output is not well-typed yet)
    route_plan: RouteResponse
    budget_plan: BudgetResponse
    safety_plan: SafetyResponse
    context_plan: ContextResponse

class ScheduledActivity(BaseModel):
    activity_id: str
    time: str  # e.g., "Morning", "10:00 AM"
    name: str
    type: str  # "attraction", "meal", "travel", "accommodation"
    description: Optional[str] = None
    cost_lkr: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    duration_minutes: Optional[int] = None

class DailySchedule(BaseModel):
    day: int
    date: Optional[str] = None
    city: str
    activities: List[ScheduledActivity] = Field(default_factory=list)
    accommodation: Optional[Dict[str, Any]] = None
    warnings: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    daily_budget_lkr: float = 0.0

class ScheduleResponse(BaseModel):
    trip_id: str
    status: str = "draft"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    itinerary: List[DailySchedule] = Field(default_factory=list)
    budget_summary: Dict[str, Any] = Field(default_factory=dict)
    overall_warnings: List[str] = Field(default_factory=list)
    planning_notes: List[str] = Field(default_factory=list)
