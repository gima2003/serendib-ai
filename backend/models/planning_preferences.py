from typing import List, Optional

from pydantic import BaseModel, Field


class PlanningPreferences(BaseModel):
    travel_style: Optional[str] = None

    accommodation_preferences: List[str] = Field(
        default_factory=list
    )

    transport_preferences: List[str] = Field(
        default_factory=list
    )

    selected_activities: List[str] = Field(
        default_factory=list
    )