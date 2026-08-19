from llm.gemini_provider import extract_with_gemini
from llm.prompts import build_profile_prompt


user_text = """
My girlfriend and I are visiting Sri Lanka for 6 days.
We have around 700 US dollars for the whole trip.
We love beaches, nature and local food.
She is vegetarian and we want a relaxed holiday.
"""

prompt = build_profile_prompt(user_text)

profile = extract_with_gemini(prompt)


print(profile.model_dump_json(indent=2))