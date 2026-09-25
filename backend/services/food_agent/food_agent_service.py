from typing import Optional, List


from services.food_agent.retrieval_service import (
    find_food_places,
)



# ==================================================
# Helpers
# ==================================================

def normalize_dietary(
    dietary
) -> Optional[str]:

    """
    Convert Agent 1 dietary format:

    ["vegetarian"]

    into:

    "vegetarian"
    """

    if not dietary:
        return None


    if isinstance(dietary, list):

        return dietary[0] if dietary else None


    return dietary





def normalize_budget(
    budget: Optional[dict]
) -> Optional[str]:

    """
    Convert traveller budget into
    restaurant budget category.
    """

    if not budget:
        return None


    amount = budget.get(
        "amount",
        0
    )


    currency = budget.get(
        "currency",
        "USD"
    )


    if currency == "USD":


        if amount < 500:

            return "cheap"


        elif amount < 1500:

            return "medium"


        else:

            return "premium"


    return None




# ==================================================
# Food Recommendation Reasoning
# ==================================================

def generate_food_reasoning(

    place: dict,

    dietary: Optional[str] = None,

    prefer_local: bool = False,

    travel_pace: Optional[str] = None,

    travel_type: Optional[str] = None,

    additional_requests: Optional[List[str]] = None

):


    reasons = []



    # ----------------------------------
    # Rating Reason
    # ----------------------------------

    rating = place.get(
        "rating"
    )


    if rating:


        if rating >= 4.5:

            reasons.append(
                f"Excellent customer rating ({rating}/5)"
            )


        elif rating >= 4.0:

            reasons.append(
                f"Good customer rating ({rating}/5)"
            )


        else:

            reasons.append(
                f"Acceptable customer rating ({rating}/5)"
            )



    # ----------------------------------
    # Local Food Preference
    # ----------------------------------

    if prefer_local:


        local_strength = str(

            place.get(
                "local_food_strength",
                ""
            )

        ).lower()



        if (

            "very high" in local_strength

            or

            "high" in local_strength

            or

            "strong" in local_strength

        ):


            reasons.append(
                "Strong authentic local food experience"
            )



    # ----------------------------------
    # Dietary Preference
    # ----------------------------------

    if dietary:


        dietary_info = str(

            place.get(
                "dietary_strength",
                ""
            )

        ).lower()



        if dietary.lower() in dietary_info:


            reasons.append(
                f"Suitable for {dietary} preference"
            )


        elif (

            dietary.lower() == "vegetarian"

            and

            "vegetarian" in dietary_info

        ):


            reasons.append(
                "Vegetarian-friendly food options available"
            )



    # ----------------------------------
    # Travel Style
    # ----------------------------------

    best_for = str(

        place.get(
            "best_for",
            ""
        )

    ).lower()



    if travel_pace == "relaxed":


        if (

            "local" in best_for

            or

            "casual" in best_for

            or

            "quiet" in best_for

        ):


            reasons.append(
                "Matches relaxed travel style"
            )



    # ----------------------------------
    # Travel Type
    # ----------------------------------

    if travel_type == "couple":


        if (

            "authentic" in best_for

            or

            "local" in best_for

        ):


            reasons.append(
                "Suitable for couple travellers"
            )



    # ----------------------------------
    # Additional Requests
    # ----------------------------------

    if additional_requests:


        for request in additional_requests:


            if (

                "authentic" in request.lower()

                and

                prefer_local

            ):


                reasons.append(
                    "Matches request for authentic Sri Lankan food"
                )

                break



    return reasons





# ==================================================
# Main Food Agent Service
# ==================================================

def recommend_food_places(

    city: str,

    budget: Optional[dict] = None,

    dietary: Optional[List[str]] = None,

    cuisine: Optional[str] = None,

    min_rating: Optional[float] = None,

    prefer_local: bool = False,

    travel_pace: Optional[str] = None,

    travel_type: Optional[str] = None,

    additional_requests: Optional[List[str]] = None,

    limit: int = 5,

):


    # ----------------------------------
    # Validation
    # ----------------------------------

    if not city or not city.strip():


        return {

            "success": False,

            "message":
                "City is required.",

            "recommendations": []

        }




    if limit <= 0:

        limit = 5



    if limit > 20:

        limit = 20




    # ----------------------------------
    # Normalize Inputs
    # ----------------------------------

    normalized_dietary = normalize_dietary(
        dietary
    )


    normalized_budget = normalize_budget(
        budget
    )




    # ----------------------------------
    # Retrieve Restaurants
    # ----------------------------------

    results = find_food_places(

        city=city,

        budget=normalized_budget,

        dietary=normalized_dietary,

        cuisine=cuisine,

        min_rating=min_rating,

        prefer_local=prefer_local,

        limit=limit

    )




    # ----------------------------------
    # No Results
    # ----------------------------------

    if not results:


        return {

            "success": True,

            "message":
                "No matching food places found.",

            "city": city,

            "recommendations": []

        }




    # ----------------------------------
    # Add Reasoning
    # ----------------------------------

    enriched_results = []



    for place in results:


        place_copy = place.copy()



        place_copy[

            "recommendation_reasoning"

        ] = generate_food_reasoning(

            place=place,

            dietary=normalized_dietary,

            prefer_local=prefer_local,

            travel_pace=travel_pace,

            travel_type=travel_type,

            additional_requests=
                additional_requests

        )



        enriched_results.append(
            place_copy
        )




    # ----------------------------------
    # Final Response
    # ----------------------------------

    return {


        "success": True,


        "message":

            f"Found {len(enriched_results)} "
            f"food recommendations for {city}.",



        "query": {


            "city": city,


            "budget":
                normalized_budget,


            "dietary":
                normalized_dietary,


            "prefer_local":
                prefer_local,


            "travel_pace":
                travel_pace,


            "travel_type":
                travel_type,


            "additional_requests":
                additional_requests

        },


        "recommendation_count":

            len(enriched_results),



        "recommendations":

            enriched_results

    }