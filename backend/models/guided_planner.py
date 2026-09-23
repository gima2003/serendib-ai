from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from models.traveller_profile import (
    TravelType,
    BudgetFlexibility,
    TravelPace,
    CrowdPreference,
)


class GuidedBudget(BaseModel):
    amount: Optional[float] = Field(
        default=None,
        gt=0
    )
    currency: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=3
    )
    flexibility: Optional[BudgetFlexibility] = None


class GuidedPlannerRequest(BaseModel):
    # Trip details
    origin: Optional[str] = Field(
        default=None,
        min_length=1
    )

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    # Traveller details
    traveller_count: Optional[int] = Field(
        default=None,
        gt=0,
        le=20
    )

    traveller_type: Optional[TravelType] = None

    # Traveller preferences
    interests: List[str] = Field(
        default_factory=list
    )

    travel_pace: Optional[TravelPace] = None

    crowd_preference: Optional[CrowdPreference] = None

    preferred_regions: List[str] = Field(
        default_factory=list
    )

    additional_notes: Optional[str] = None

    # Budget
    budget: Optional[GuidedBudget] = None

    # Planning preferences
    travel_style: Optional[str] = None

    accommodation_preferences: List[str] = Field(
        default_factory=list
    )

    transport_preferences: List[str] = Field(
        default_factory=list
    )

    # Food
    dietary_preference: Optional[str] = None

    food_preferences: List[str] = Field(
        default_factory=list
    )

    # Activities
    selected_activities: List[str] = Field(
        default_factory=list
    )