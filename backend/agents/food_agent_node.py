from services.food_agent.food_agent_service import (
    recommend_food_places,
)

from services.food_agent.food_response_formatter import (
    format_food_response,
)



def food_agent_node(state):

    # ==================================================
    # 1. Get Traveller Profile (Agent 1)
    # ==================================================

    profile = state.get(
        "profile",
        {}
    )


    dietary_requirements = profile.get(
        "dietary_requirements",
        []
    )


    food_preferences = profile.get(
        "food_preferences",
        []
    )


    budget = profile.get(
        "budget",
        None
    )


    travel_type = profile.get(
        "travel_type",
        None
    )


    travel_pace = profile.get(
        "travel_pace",
        None
    )


    additional_requests = profile.get(
        "additional_requests",
        []
    )



    # ==================================================
    # 2. Get Destination Recommendations (Agent 2)
    # ==================================================

    destinations = (
        state.get(
            "result",
            {}
        )
        .get(
            "recommended_destinations",
            []
        )
    )


    food_recommendations = []



    # ==================================================
    # 3. Generate Food Recommendations
    # ==================================================

    for destination in destinations:


        city = destination.get(
            "destination"
        )


        if not city:
            continue



        destination_score = destination.get(
            "score"
        )


        attractions = destination.get(
            "attractions",
            []
        )



        # ==============================================
        # Call Food Recommendation Service
        # ==============================================

        response = recommend_food_places(

            city=city,

            # Agent 1 preferences
            dietary=dietary_requirements,

            budget=budget,

            prefer_local=(
                "local_food"
                in food_preferences
            ),

            travel_pace=travel_pace,

            travel_type=travel_type,

            additional_requests=additional_requests,

            limit=5

        )



        # ==============================================
        # DEBUG RAW RESPONSE
        # ==============================================

        print(
            "\n================ RAW FOOD RESPONSE ================"
        )


        if response.get(
            "recommendations"
        ):

            print(
                response["recommendations"][0]
            )

        else:

            print(
                "No food recommendations returned"
            )


        print(
            "===================================================\n"
        )



        # ==============================================
        # Format output for next agent
        # ==============================================

        formatted = {


            "destination": city,


            "destination_score":
                destination_score,



            "traveller_context": {


                "travel_type":
                    travel_type,


                "travel_pace":
                    travel_pace,


                "dietary_requirements":
                    dietary_requirements,


                "food_preferences":
                    food_preferences,


                "additional_requests":
                    additional_requests

            },



            "destination_context": {


                "attractions": [

                    {

                        "name":
                            attraction.get(
                                "name"
                            ),


                        "category":
                            attraction.get(
                                "category"
                            ),


                        "sub_category":
                            attraction.get(
                                "sub_category"
                            )

                    }

                    for attraction in attractions

                ]

            },



            "restaurants":

                format_food_response(

                    response.get(
                        "recommendations",
                        []
                    )

                )

        }



        food_recommendations.append(
            formatted
        )



    # ==================================================
    # 4. Update Shared Agent State
    # ==================================================

    state["food_recommendations"] = (
        food_recommendations
    )


    return state