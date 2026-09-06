from typing import List, Optional
from pydantic import BaseModel, Field


class DestinationPreferences(BaseModel):
    interests: List[str] = Field(default_factory=list)

    preferred_destinations: List[str] = Field(
        default_factory=list
    )

    crowd_preference: Optional[str] = None

    travel_pace: Optional[str] = None

    duration_days: Optional[int] = Field(
        default=None,
        ge=1
    )

    accessibility_requirements: List[str] = Field(
        default_factory=list
    )