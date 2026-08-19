import os

from dotenv import load_dotenv
from google import genai

from models.traveller_profile import (
    LLMTravellerProfile,
    TravellerProfile,
)


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GENAI_API_KEY")
)


def extract_with_gemini(prompt: str) -> TravellerProfile:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": LLMTravellerProfile,
        },
    )

    llm_profile = LLMTravellerProfile.model_validate_json(
        response.text
    )

    return TravellerProfile.model_validate(
        llm_profile.model_dump()
    )