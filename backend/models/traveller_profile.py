from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


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
    
    # Planning preferences (usually from guided planner or extracted)
    travel_style: Optional[str] = None
    
    accommodation_preferences: List[str] = Field(
        default_factory=list
    )
    
    transport_preferences: List[str] = Field(
        default_factory=list
    )

    # Date fields — extracted from natural language (e.g. "November 3rd")
    start_date: Optional[str] = Field(
        default=None,
        description="ISO date string YYYY-MM-DD for trip start"
    )

    end_date: Optional[str] = Field(
        default=None,
        description="ISO date string YYYY-MM-DD for trip end (auto-calculated if not given)"
    )

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def coerce_date_to_str(cls, v):
        """Accept datetime.date/datetime.datetime objects and convert to ISO strings."""
        if v is None:
            return None
        if hasattr(v, "strftime"):
            return v.strftime("%Y-%m-%d")
        return str(v)


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

    # Date fields
    start_date: Optional[str] = None  # ISO string YYYY-MM-DD
    end_date: Optional[str] = None    # ISO string YYYY-MM-DD (auto-calculated if missing)

    @field_validator(
        'interests',
        'dietary_requirements',
        'food_preferences',
        'preferred_destinations',
        'must_visit_destinations',
        'avoidances',
        'accessibility_requirements',
        'additional_requests',
        mode='before'
    )
    @classmethod
    def coerce_none_to_list(cls, v):
        if v is None:
            return []
        return v

class TravellerTextRequest(BaseModel):
    text: str = Field(min_length=1)