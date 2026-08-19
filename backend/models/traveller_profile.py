from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


# --------------------------------------------------
# Controlled vocabularies
# --------------------------------------------------

class TravelType(str, Enum):
    solo = "solo"
    couple = "couple"
    family = "family"
    friends = "friends"
    business = "business"
    other = "other"


class BudgetScope(str, Enum):
    total_trip = "total_trip"
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
    balanced = "balanced"
    fast = "fast"


class CrowdPreference(str, Enum):
    avoid = "avoid"
    neutral = "neutral"
    enjoy = "enjoy"


# --------------------------------------------------
# Application / validated models
# --------------------------------------------------

class Budget(BaseModel):
    amount: Optional[float] = Field(
        default=None,
        gt=0
    )

    currency: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=3
    )

    scope: Optional[BudgetScope] = None

    flexibility: Optional[BudgetFlexibility] = None


class Interest(BaseModel):
    name: str = Field(
        min_length=1
    )

    preference: Optional[PreferenceStrength] = None


class TravellerProfile(BaseModel):
    duration_days: Optional[int] = Field(
        default=None,
        gt=0,
        le=60
    )

    traveller_count: Optional[int] = Field(
        default=None,
        gt=0,
        le=20
    )

    travel_type: Optional[TravelType] = None

    starting_location: Optional[str] = Field(
        default=None,
        min_length=1
    )

    budget: Optional[Budget] = None

    interests: List[Interest] = Field(
        default_factory=list
    )

    dietary_requirements: List[str] = Field(
        default_factory=list
    )

    food_preferences: List[str] = Field(
        default_factory=list
    )

    travel_pace: Optional[TravelPace] = None

    crowd_preference: Optional[CrowdPreference] = None

    preferred_destinations: List[str] = Field(
        default_factory=list
    )

    must_visit_destinations: List[str] = Field(
        default_factory=list
    )

    avoidances: List[str] = Field(
        default_factory=list
    )

    accessibility_requirements: List[str] = Field(
        default_factory=list
    )

    additional_requests: List[str] = Field(
        default_factory=list
    )


# --------------------------------------------------
# LLM-facing models
# --------------------------------------------------

class LLMBudget(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    scope: Optional[BudgetScope] = None
    flexibility: Optional[BudgetFlexibility] = None


class LLMInterest(BaseModel):
    name: str

    preference: Optional[PreferenceStrength] = None


class LLMTravellerProfile(BaseModel):
    duration_days: Optional[int] = None
    traveller_count: Optional[int] = None

    travel_type: Optional[TravelType] = None
    starting_location: Optional[str] = None

    budget: Optional[LLMBudget] = None

    interests: List[LLMInterest] = Field(
        default_factory=list
    )

    dietary_requirements: List[str] = Field(
        default_factory=list
    )

    food_preferences: List[str] = Field(
        default_factory=list
    )

    travel_pace: Optional[TravelPace] = None

    crowd_preference: Optional[CrowdPreference] = None

    preferred_destinations: List[str] = Field(
        default_factory=list
    )

    must_visit_destinations: List[str] = Field(
        default_factory=list
    )

    avoidances: List[str] = Field(
        default_factory=list
    )

    accessibility_requirements: List[str] = Field(
        default_factory=list
    )

    additional_requests: List[str] = Field(
        default_factory=list
    )