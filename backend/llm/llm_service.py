from models.traveller_profile import TravellerProfile

from llm.gemini_provider import extract_with_gemini
from llm.groq_provider import extract_with_groq

class LLMServiceError(Exception):
    pass

def extract_traveller_profile(
        prompt: str,
) -> TravellerProfile:
    try:
        return extract_with_groq(prompt)
    except Exception as gemini_error:
        print(
            f"Gemini provider failede: {gemini_error}"
        )

    try:
        return extract_with_groq(prompt)

    except Exception as groq_error:
        print(
            f"Groq provider failed: {groq_error}"
        )

        raise LLMServiceError(
            "All configured LLM providers failed."
        )