import os
import json

from dotenv import load_dotenv
from groq import Groq

from models.traveller_profile import (
    LLMTravellerProfile,
    TravellerProfile,
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_with_groq(prompt: str) -> TravellerProfile:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema":{
                "name": "traveller_profile",
                "schema": LLMTravellerProfile.model_json_schema(),
            },
        },
    )

    content = completion.choices[0].message.content

    profile_data = json.loads(content)

    llm_profile = LLMTravellerProfile.model_validate(
        profile_data
    )

    return TravellerProfile.model_validate(
        llm_profile.model_dump()
    )