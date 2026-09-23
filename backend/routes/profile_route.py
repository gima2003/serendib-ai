from models.guided_planner import GuidedPlannerRequest
from services.guided_planner_service import (
    build_guided_profile_state,
)

from fastapi import APIRouter, HTTPException

from llm.llm_service import (
    LLMServiceError,
    extract_traveller_profile
)

from llm.prompts import build_profile_prompt

from models.traveller_profile import (
    TravellerProfile,
    TravellerTextRequest,
)

from models.profile_conversation import (
    AssistantState,
    ProfileConversationResponse,
)

from services.profile_state_service import (
    create_profile_state,
)

from models.clarification_request import (
    ClarificationPermissionRequest,
)

from services.clarification_controller import (
    CLARIFICATION_PERMISSION_MESSAGE,
    handle_clarification_permission as process_clarification_permission,
    process_clarification_answer,
    generate_next_clarification_question,
)

from models.clarification_answer_request import (
    ClarificationAnswerRequest,
)

from models.profile_state import ProfileState

router = APIRouter(
    prefix="/profile",
    tags=["Traveller Profile"]
)

@router.post("/")
async def create_profile(profile: TravellerProfile):
    return{
        "message": "Traveller profile reviewed successfully",
        "profile": profile
    }

@router.post(
    "/extract",
    response_model=ProfileConversationResponse,
)
async def extract_profile(
    request: TravellerTextRequest,
):
    try:
        prompt = build_profile_prompt(
            request.text
        )

        profile = extract_traveller_profile(
            prompt
        )

        profile_state = create_profile_state(
            profile
        )

        if profile_state.profile_status == "ready":

            assistant = AssistantState(
                visible=False,
                message=None,
                current_context=None,
            )

        else:

            assistant = AssistantState(
                visible=True,
                message=CLARIFICATION_PERMISSION_MESSAGE,
                current_context=None,
            )

        return ProfileConversationResponse(
            status=profile_state.profile_status,
            profile=profile_state.traveller_profile,
            readiness=profile_state.profile_readiness,
            assistant=assistant,
        )

    except LLMServiceError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

@router.post(
    "/guided",
    response_model=ProfileState,
)
async def create_guided_profile(
    request: GuidedPlannerRequest,
):
    return build_guided_profile_state(request)

@router.post(
    "/clarification/permission",
    response_model=ProfileConversationResponse,
)
async def handle_clarification_permission(
    request: ClarificationPermissionRequest,
):
    try:
        profile_state = create_profile_state(
            request.profile
        )

        result_type, message = (
            process_clarification_permission(
                user_response=request.user_response,
                readiness=profile_state.profile_readiness,
            )
        )

        # User declined clarification.
        if result_type == "finalize_available_profile":

            assistant = AssistantState(
                visible=False,
                message=None,
                current_context=None,
            )

            return ProfileConversationResponse(
                status="finalized_with_available_profile",
                profile=profile_state.traveller_profile,
                readiness=profile_state.profile_readiness,
                assistant=assistant,
            )

        # User's response was unclear.
        if result_type == "request_clear_permission":

            assistant = AssistantState(
                visible=True,
                message=message,
                current_context=None,
            )

            return ProfileConversationResponse(
                status="needs_clarification",
                profile=profile_state.traveller_profile,
                readiness=profile_state.profile_readiness,
                assistant=assistant,
            )

        # User agreed to clarification.
        assistant = AssistantState(
            visible=True,
            message=message,
            current_context=result_type,
        )

        return ProfileConversationResponse(
            status="needs_clarification",
            profile=profile_state.traveller_profile,
            readiness=profile_state.profile_readiness,
            assistant=assistant,
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

@router.post(
    "/clarification/answer",
    response_model=ProfileConversationResponse,
)
async def handle_clarification_answer(
    request: ClarificationAnswerRequest,
):
    try:
        (
            updated_profile,
            readiness,
            next_context,
        ) = process_clarification_answer(
            profile=request.profile,
            current_context=request.current_context,
            user_answer=request.user_answer,
        )

        # Profile is now ready.
        if readiness.ready:

            assistant = AssistantState(
                visible=False,
                message=None,
                current_context=None,
            )

            return ProfileConversationResponse(
                status="ready",
                profile=updated_profile,
                readiness=readiness,
                assistant=assistant,
            )

        # More information is still required.
        next_question = (
            generate_next_clarification_question(
                next_context
            )
        )

        assistant = AssistantState(
            visible=True,
            message=next_question,
            current_context=next_context,
        )

        return ProfileConversationResponse(
            status="needs_clarification",
            profile=updated_profile,
            readiness=readiness,
            assistant=assistant,
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )