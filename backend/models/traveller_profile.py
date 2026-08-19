from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class TravelType(str, Enum):
    solo = "solo"
    couple = "couple"
    family = "family"
    friends = "friends"
    business = "business"
    other = "other"

class BudgetScope(str, Enum):
    toatl_trip = "total_trip"
    per_person = "per_person"

class BudgetFlexibility(str, Enum):
    strict = "strict"
    moderate = "moderate"
    flexible = "flexible"
    
class PreferenceStrength(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TravelPace(str, Enum):
    relaxed = "relaxed"
    moderate = "moderate"
    fast = "fast"

class CrowdPreference(str, Enum):
    avoid = "avoid"
    neutral = "neutral"
    enjoy = "enjoy"

class Budget(BaseModel):
    amount: float = Field(gt = 0)
    currency: str = Field(min_length=3, max_length=3)
    scope: BudgetScope
    flexibility: BudgetFlexibility

class Interest(BaseModel):
    name: str = Field(min_length=1)
    preference: PreferenceStrength

class TravellerProfile(BaseModel):
    duration_days: Optional[int] = Field(default=None, gt=0, le=60)
    traveller_count: Optional[int] = Field(default=None, gt=0, le=20)

    travel_type: Optional[TravelType] = None
    starting_location: Optional[str] = Field(default=None, min_length=1)

    budget: Optional[Budget] = None

    interests: List[Interest] = Field(default_factory=list)

    dietary_requirements: List[str] = Field(default_factory=list)
    food_preferences: List[str] = Field(default_factory=list)

    travel_pace: Optional[TravelPace] = None
    crowd_preference: Optional[CrowdPreference] = None

    preferred_destinations: List[str] = Field(default_factory=list)
    must_visit_destinations: List[str] = Field(default_factory=list)

    avoidances: List[str] = Field(default_factory=list)
    accessibility_requirements: List[str] = Field(default_factory=list)

    additional_requests: List[str] = Field(default_factory=list)