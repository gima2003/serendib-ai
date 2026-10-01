from models.traveller_profile import TravellerProfile

from llm.gemini_provider import (
    extract_with_gemini,
    validate_with_gemini,
)

from llm.groq_provider import (
    extract_with_groq,
    validate_with_groq,
)

from services.profile_normalizer import normalize_traveller_profile

class LLMServiceError(Exception):
    pass

def extract_traveller_profile(
        prompt: str,
) -> TravellerProfile:
    try:
        profile = extract_with_gemini(prompt)

        return normalize_traveller_profile(profile)
    
    except Exception as gemini_error:
        print(
            f"Gemini provider failede: {gemini_error}"
        )

    try:
        profile = extract_with_groq(prompt)

        return normalize_traveller_profile(profile)

    except Exception as groq_error:
        print(
            f"Groq provider failed: {groq_error}"
        )

        raise LLMServiceError(
            "All configured LLM providers failed."
        )

def update_traveller_profile(
        existing_profile_json: str,
        missing_context: str,
        user_answer: str,
) -> TravellerProfile:

    prompt = build_profile_update_prompt(
        existing_profile_json,
        missing_context,
        user_answer,
    )

    try:
        profile = extract_with_gemini(prompt)

        return normalize_traveller_profile(profile)

    except Exception as gemini_error:
        print(
            f"Gemini profile update failed: {gemini_error}"
        )

    try:
        profile = extract_with_groq(prompt)

        return normalize_traveller_profile(profile)

    except Exception as groq_error:
        print(
            f"Groq profile update failed: {groq_error}"
        )

        raise LLMServiceError(
            "All configured LLM providers failed."
        )


def validate_travel_prompt(text: str) -> bool:

    validation_prompt = f"""
You are a travel request validator.

Determine whether the user's request is related to travel planning.

A request is TRAVEL_RELATED if it involves things such as:
- destinations
- tourism
- attractions
- activities
- trips
- itineraries
- travel dates or duration
- transportation or routes
- accommodation
- restaurants or food while travelling
- travel budget
- traveller preferences

Return ONLY one word:

YES

or

NO

User request:
{text}
"""

    try:

        result = validate_with_gemini(
            validation_prompt
        )

        result = result.upper().strip()

        if result == "YES":
            return True

        if result == "NO":
            return False

        raise ValueError(
            f"Unexpected validation response: {result}"
        )

    except Exception as gemini_error:

        print(
            f"Gemini travel validation failed: {gemini_error}"
        )

    try:

        result = validate_with_groq(
            validation_prompt
        )

        result = result.upper().strip()

        if result == "YES":
            return True

        if result == "NO":
            return False

        raise ValueError(
            f"Unexpected validation response: {result}"
        )

    except Exception as groq_error:

        print(
            f"Groq travel validation failed: {groq_error}"
        )

        raise LLMServiceError(
            "All configured LLM providers failed."
        )