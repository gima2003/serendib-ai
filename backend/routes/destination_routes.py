from fastapi import APIRouter, HTTPException

from schemas.destination_schemas import DestinationPreferences

from services.destination.destination_recommender import (
    recommend_destinations
)


router = APIRouter(
    prefix="/api/destination",
    tags=["Destination Intelligence"]
)


@router.post("/recommend")
def recommend_destination(
    preferences: DestinationPreferences
):

    try:

        result = recommend_destinations(
            interests=preferences.interests,
            top_destinations=5,
            top_attractions=5,
            debug=False
        )

        return {
            "status": "success",
            "input": preferences.model_dump(),
            "result": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )