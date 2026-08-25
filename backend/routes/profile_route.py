from fastapi import APIRouter
from models.traveller_profile import TravellerProfile
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
    response_model=TravellerProfile,
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

        return profile

    except LLMServiceError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )