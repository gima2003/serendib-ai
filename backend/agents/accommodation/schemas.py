from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AccommodationPriceInfo(BaseModel):
    type: str = "unavailable" # "source_provided", "estimated_range", "unavailable"
    price_per_night_lkr: Optional[float] = None
    min_per_night_lkr: Optional[float] = None
    max_per_night_lkr: Optional[float] = None
    estimated_price_per_night_lkr: Optional[float] = None
    price_basis: str = "unknown" # "room", "person", "unit", "unknown"
    source: Optional[str] = None
    confidence: Optional[str] = None

class AccommodationCandidate(BaseModel):
    accommodation_id: str
    name: str
    city: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accommodation_type: str = "accommodation"
    rating: Optional[float] = None
    review_count: Optional[int] = None
    amenities: List[str] = Field(default_factory=list)
    source: str
    source_confidence: str = "medium"
    price_information: AccommodationPriceInfo = Field(default_factory=AccommodationPriceInfo)
    distance_information: Optional[Dict[str, Any]] = None
    capacity_status: str = "unknown"
    maximum_guests: Optional[int] = None
    limitations: List[str] = Field(default_factory=list)

class AccommodationRecommendationResult(AccommodationCandidate):
    recommendation_score: float = 0.0
    recommendation_reasons: List[str] = Field(default_factory=list)
    is_selected: bool = False

class DestinationAccommodation(BaseModel):
    city: str
    nights: int
    selected_accommodation_id: Optional[str] = None
    hotel_options: List[AccommodationRecommendationResult] = Field(default_factory=list)

class AccommodationResponse(BaseModel):
    status: str = "success"
    accommodation_plan: List[DestinationAccommodation] = Field(default_factory=list)

class StayRequest(BaseModel):
    city: str
    nights: int

class BudgetRequest(BaseModel):
    amount: float
    currency: str

class AccommodationRequest(BaseModel):
    traveller_count: int = 1
    travel_type: str = "solo"
    travel_pace: str = "moderate"
    interests: List[str] = Field(default_factory=list)
    budget: BudgetRequest
    stays: List[StayRequest]
