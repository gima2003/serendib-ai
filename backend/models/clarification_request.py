from pydantic import BaseModel

from models.traveller_profile import TravellerProfile


class ClarificationPermissionRequest(BaseModel):
    # The current traveller profile produced by Agent 1.
    profile: TravellerProfile

    # The traveller's response to the permission message.
    user_response: str