def prepare_agent4_input(
    destination_result
):

    destinations = []

    for destination in destination_result.get(
        "recommended_destinations",
        []
    ):

        attractions = []

        for attraction in destination.get(
            "attractions",
            []
        ):

            attractions.append(
                {
                    "name":
                        attraction.get(
                            "name"
                        ),

                    "category":
                        attraction.get(
                            "category"
                        ),

                    "indoor_outdoor":
                        attraction.get(
                            "indoor_outdoor"
                        ),

                    "estimated_entry_cost":
                        attraction.get(
                            "entry_costs",
                            []
                        )
                }
            )


        destinations.append(
            {
                "city":
                    destination.get(
                        "destination"
                    ),

                "recommendation_score":
                    destination.get(
                        "score"
                    ),

                "attractions":
                    attractions
            }
        )


    return {
        "destinations":
            destinations
    }