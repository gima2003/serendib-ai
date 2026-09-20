from models.traveller_profile import TravellerProfile

from llm.gemini_provider import extract_with_gemini
from llm.groq_provider import extract_with_groq

from llm.prompts import build_profile_update_prompt

from services.profile_normalizer import normalize_traveller_profile


class ProfileUpdateError(Exception):
    pass


def update_traveller_profile(
    existing_profile: TravellerProfile,
    missing_context: str,
    user_answer: str,
) -> TravellerProfile:

    existing_profile_json = (
        existing_profile.model_dump_json(indent=2)
    )

    prompt = build_profile_update_prompt(
        existing_profile_json=existing_profile_json,
        missing_context=missing_context,
        user_answer=user_answer,
    )

    try:
        updated_profile = extract_with_gemini(
            prompt
        )

        return normalize_traveller_profile(
            updated_profile
        )

    except Exception as gemini_error:
        print(
            f"Gemini profile update failed: {gemini_error}"
        )

    try:
        updated_profile = extract_with_groq(
            prompt
        )

        return normalize_traveller_profile(
            updated_profile
        )

    except Exception as groq_error:
        print(
            f"Groq profile update failed: {groq_error}"
        )

        raise ProfileUpdateError(
            "Unable to update traveller profile."
        )