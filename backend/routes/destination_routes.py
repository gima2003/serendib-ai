from fastapi import APIRouter, HTTPException

from schemas.destination_schemas import DestinationPreferences

from services.destination.destination_recommender import (
    recommend_destinations,
    recommend_from_preferred_destinations
)

from services.destination.cost_loader import load_costs

from services.destination.destination_validator import validate_destination


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

        # =================================================
        # Case 1:
        # User explicitly selected destination(s)
        # Highest priority
        # =================================================

        if preferences.preferred_destinations:

            validated_destinations = []


            available_destinations = [
                "Sigiriya",
                "Ella",
                "Kandy",
                "Nuwara Eliya",
                "Colombo",
                "Galle",
                "Arugam Bay",
                "Jaffna",
                "Mirissa",
                "Anuradhapura",
                "Dambulla",
                "Yala",
                "Bandarawela"
            ]


            for destination in preferences.preferred_destinations:

                validation = validate_destination(
                    destination,
                    available_destinations
                )


                if validation["status"] != "valid":

                    return {
                        "status": "error",
                        "message": "Invalid destination",
                        "destination": destination,
                        "validation": validation
                    }


                validated_destinations.append(
                    validation["destination"]
                )


            result = recommend_from_preferred_destinations(
                destinations=validated_destinations,
                interests=preferences.interests,
                top_attractions=5
            )

        # =================================================
        # Case 2:
        # No destination selected
        # Recommend based on interests
        # =================================================

        elif preferences.interests:

            result = recommend_destinations(
                interests=preferences.interests,
                top_destinations=5,
                top_attractions=5,
                debug=False
            )


        # =================================================
        # Case 3:
        # No useful preference
        # =================================================

        else:

            result = {

                "input_interests": [],

                "matched_experiences": [],

                "unmatched_interests": [],

                "recommended_destinations": []

            }



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