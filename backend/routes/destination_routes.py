from fastapi import APIRouter, HTTPException

from schemas.destination_schemas import DestinationPreferences

from services.destination.destination_recommender import (
    recommend_destinations
)

from services.destination.cost_loader import (
    load_costs
)


router = APIRouter(
    prefix="/api/destination",
    tags=["Destination Intelligence"]
)


# =====================================================
# Main Agent 2 Recommendation API
# =====================================================

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


# =====================================================
# Dataset Information APIs
# (Useful for demonstration/testing)
# =====================================================


@router.get("/attractions")
def get_attractions():

    return {
        "status": "success",
        "dataset": "Sri Lanka Attractions",
        "total_attractions": 87
    }



@router.get("/experiences")
def get_experiences():

    return {
        "status": "success",
        "dataset": "Attraction Experience Mapping",
        "total_experiences": 33,
        "relationships": 279
    }



@router.get("/costs")
def get_cost_information():

    try:

        costs = load_costs()

        return {
            "status": "success",
            "dataset": "Attraction Entry Costs",
            "data": costs
        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )