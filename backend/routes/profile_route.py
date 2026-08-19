from fastapi import APIRouter
from models.traveller_profile import TravellerProfile

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