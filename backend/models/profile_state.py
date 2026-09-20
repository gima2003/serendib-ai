from typing import Literal
from pydantic import BaseModel

from models.traveller_profile import TravellerProfile
from models.profile_readiness import profileReadiness


class ProfileState(BaseModel):
    # Current structured traveller profile.
    traveller_profile: TravellerProfile

    # Shows whether downstream agents have enough context.
    profile_readiness: profileReadiness

    # Used by LangGraph to decide the next workflow path.
    profile_status: Literal[
        "ready",
        "needs_clarification",
        "finalized_with_available_profile",
    ]

    # Missing topic currently being clarified.
    # None when no clarification question is active.
    current_clarification_context: str | None = None

    # Tracks whether the traveller agreed to answer
    # additional clarification questions.
    clarification_permission_granted: bool | None = None