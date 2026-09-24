from typing import List
from pydantic import BaseModel, Field

class profileReadiness(BaseModel):
    ready: bool = False

    trip_basics_ready: bool = False
    destination_ready: bool = False
    food_ready: bool = False
    planner_ready: bool = False

    missing_context: List[str] = Field(
        default_factory=list
    )