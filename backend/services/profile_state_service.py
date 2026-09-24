from models.traveller_profile import TravellerProfile
from models.profile_state import ProfileState

from services.profile_readiness_service import (
    check_profile_readiness,
)


# Creates Agent 1's initial workflow state from
# the extracted and normalized traveller profile.
def create_profile_state(
    profile: TravellerProfile,
) -> ProfileState:

    # Check whether the profile contains enough
    # information for downstream agents.
    readiness = check_profile_readiness(
        profile
    )

    # Decide the workflow status.
    if readiness.ready:
        profile_status = "ready"
    else:
        profile_status = "needs_clarification"

    # Build the state that can later be stored
    # inside the LangGraph shared state.
    return ProfileState(
        traveller_profile=profile,
        profile_readiness=readiness,
        profile_status=profile_status,
        current_clarification_context=None,
        clarification_permission_granted=None,
    )