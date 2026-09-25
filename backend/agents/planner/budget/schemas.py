from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TransportOption(BaseModel):
    mode: str
    provider: Optional[str] = None
    estimated_cost_lkr: float = 0.0
    price_available: bool
    coverage: str = "unavailable" # "complete", "partial", "unavailable"
    reason: List[str] = Field(default_factory=list)
    breakdown: Dict[str, Any] = Field(default_factory=dict)

class TransportCostBreakdown(BaseModel):
    total_transport_lkr: float
    selected_mode: str
    options: List[TransportOption] = Field(default_factory=list)

class CostBreakdown(BaseModel):
    transport_lkr: float = 0.0
    accommodation_lkr: float = 0.0
    food_lkr: float = 0.0
    attractions_lkr: float = 0.0
    contingency_lkr: float = 0.0

class SavingsOpportunity(BaseModel):
    category: str
    description: str
    potential_saving_lkr: float
    alternative_option: str

class RecommendedTransport(BaseModel):
    recommended_mode: str
    reason: List[str] = Field(default_factory=list)
    estimated_cost_lkr: float
    
class BudgetResponse(BaseModel):
    trip_id: str
    available_budget_lkr: float
    cost_breakdown: CostBreakdown
    estimated_total_cost_lkr: float
    remaining_budget_lkr: float
    budget_utilization_percent: float
    within_budget: bool
    transport_comparison: List[TransportOption] = Field(default_factory=list)
    recommended_transport: RecommendedTransport
    savings_opportunities: List[SavingsOpportunity] = Field(default_factory=list)
    data_sources: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

# Mock Input Schemas for Orchestrator processing
class Member1Budget(BaseModel):
    amount: float
    currency: str = "LKR"

class Member1Travellers(BaseModel):
    adults: int = 1
    children: int = 0

class Member1Profile(BaseModel):
    trip_id: str
    duration_days: int
    travellers: Member1Travellers
    budget: Member1Budget
    travel_style: str = "moderate"
    transport_preferences: List[str] = Field(default_factory=list)

class Attraction(BaseModel):
    name: str
    estimated_entry_cost_lkr: float = 0.0

class Destination(BaseModel):
    city: str
    attractions: List[Attraction] = Field(default_factory=list)

class Member2Destinations(BaseModel):
    destinations: List[Destination]

class FoodRecommendation(BaseModel):
    estimated_cost_per_person_lkr: float = 0.0

class AccommodationRecommendation(BaseModel):
    estimated_cost_per_night_lkr: float = 0.0
    recommended_nights: int = 1

class Member3FoodAcc(BaseModel):
    food_recommendations: List[FoodRecommendation] = Field(default_factory=list)
    accommodation_recommendations: List[AccommodationRecommendation] = Field(default_factory=list)
