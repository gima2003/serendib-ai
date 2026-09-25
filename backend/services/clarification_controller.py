from models.profile_readiness import profileReadiness
from models.traveller_profile import TravellerProfile

from services.profile_update_service import (
    update_traveller_profile,
)

from services.profile_readiness_service import (
    check_profile_readiness,
    get_next_missing_context,
)

from llm.prompts import build_clarification_prompt

from services.clarification_service import (
    generate_clarification_question,
)

from models.clarification_decision import ClarificationDecision


CLARIFICATION_PERMISSION_MESSAGE = (
    "I’ve got the main idea for your trip. "
    "Before I complete your recommendations and travel plan, "
    "could I ask you a few short questions to personalize it better?"
)


# Checks whether the current traveller profile still needs clarification.
def needs_clarification(
    readiness: profileReadiness
) -> bool:

    return not readiness.ready


# Returns the permission message only when clarification is required.
# If the profile is already ready, it returns None.
def get_clarification_permission_message(
    readiness: profileReadiness
) -> str | None:

    if not needs_clarification(readiness):
        return None

    return CLARIFICATION_PERMISSION_MESSAGE


# Common user responses that mean the traveller agrees
# to answer clarification questions.
POSITIVE_RESPONSES = {
    "yes",
    "yeah",
    "yep",
    "sure",
    "okay",
    "ok",
    "go ahead",
    "of course",
}


# Common user responses that mean the traveller does not
# want to continue with clarification questions.
NEGATIVE_RESPONSES = {
    "no",
    "nope",
    "skip",
    "skip it",
    "continue",
    "just continue",
    "not now",
}


# Converts the user's permission response into:
# True  -> user agrees
# False -> user refuses
# None  -> response is unclear
def parse_clarification_permission(
    user_response: str
) -> bool | None:

    cleaned_response = user_response.strip().lower()

    if cleaned_response in POSITIVE_RESPONSES:
        return True

    if cleaned_response in NEGATIVE_RESPONSES:
        return False

    return None


# Processes one clarification answer.
# It updates the existing traveller profile,
# checks readiness again,
# and finds the next missing context if more information is needed.
def process_clarification_answer(
    profile: TravellerProfile,
    current_context: str,
    user_answer: str,
) -> tuple[
    TravellerProfile,
    profileReadiness,
    str | None,
]:

    updated_profile = update_traveller_profile(
        existing_profile=profile,
        missing_context=current_context,
        user_answer=user_answer,
    )

    readiness = check_profile_readiness(
        updated_profile
    )

    next_context = get_next_missing_context(
        readiness.missing_context
    )

    return (
        updated_profile,
        readiness,
        next_context,
    )


# Creates the next natural-language clarification question.
# If no missing context remains, it returns None.
def generate_next_clarification_question(
    next_context: str | None
) -> str | None:

    if next_context is None:
        return None

    prompt = build_clarification_prompt(
        next_context
    )

    question = generate_clarification_question(
        prompt
    )

    return question

#converts the user's permission response into clear
# action that the clarification workflow can follow

def get_clarification_decision(
        user_response: str
) -> ClarificationDecision:

    permission = parse_clarification_permission(
        user_response
    )

    if permission is True:
        return ClarificationDecision(
            action="continue_clarification"
        )

    if permission is False:
        return ClarificationDecision(
            action="finalize_available_profile"
        )

    return ClarificationDecision(
        action="request_clear_permission",
        message=(
            "Would you like to answer a few short questions "
            "before we continue? You can say yes or no."
        ),
    )

# Handles the traveller's response to the clarification permission message.
# It either starts clarification, stop clarificatio,
# or ask the traveller for a clear yes/no response

def handle_clarification_permission(
        user_response: str,
        readiness: profileReadiness,
) -> tuple[str, str | None ]:

    decision = get_clarification_decision(
        user_response
    )

    # User does not want to answer more questions.
    if decision.action == "finalize_available_profile":
        return (
            "finalize_available_profile",
            None,
        )

    # User's response was unclear.
    if decision.action == "request_clear_permission":
        return (
            "request_clear_permission",
            decision.message,
        )

    # User agreed to clarification.
    next_context = get_next_missing_context(
        readiness.missing_context
    )

    # Safety check in case nothing is actually missing.
    if next_context is None:
        return (
            "finalize_available_profile",
            None,
        )

    question = generate_next_clarification_question(
        next_context
    )

    return (
        next_context,
        question,
    )

    