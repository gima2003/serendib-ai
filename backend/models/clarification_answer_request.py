from pydantic import BaseModel

from models.traveller_profile import TravellerProfile


class ClarificationAnswerRequest(BaseModel):
    # Current profile before processing the new answer.
    profile: TravellerProfile

    # The clarification topic that was asked.
    # Example: "duration_days", "food_preferences".
    current_context: str

    # The traveller's answer to that question.
    user_answer: str