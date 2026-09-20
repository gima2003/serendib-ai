from typing import Literal

from pydantic import BaseModel

from models.traveller_profile import TravellerProfile
from models.profile_readiness import profileReadiness


class AssistantState(BaseModel):
    # Controls whether the frontend should show
    # the floating clarification assistant.
    visible: bool = False

    # Message or question shown to the traveller.
    message: str | None = None

    # The clarification topic currently being handled.
    current_context: str | None = None


class ProfileConversationResponse(BaseModel):
    # Tells the frontend what Agent 1 needs to do next.
    status: Literal[
        "ready",
        "needs_clarification",
        "finalized_with_available_profile",
    ]

    # Current structured traveller information.
    profile: TravellerProfile

    # Current readiness information.
    readiness: profileReadiness

    # State of the floating clarification assistant.
    assistant: AssistantState