from agents.food_agent_node import food_agent_node



# ==========================================
# Simulated Agent 1 + Agent 2 State
# ==========================================

state = {

    "profile": {

        "duration_days": 6,

        "traveller_count": 2,

        "travel_type": "couple",

        "budget": {

            "amount": 900,

            "currency": "USD",

            "scope": "total_trip"

        },


        "dietary_requirements": [

            "vegetarian"

        ],


        "food_preferences": [

            "local_food"

        ],


        "travel_pace": "relaxed",


        "additional_requests": [

            "Want to try authentic Sri Lankan local dishes"

        ]

    },


    # Agent 2 Output

    "result": {

        "recommended_destinations": [

            {

                "destination": "Ella",

                "score": 0.868,

                "attractions": [

                    {

                        "name": "Little Adam's Peak",

                        "category": "Nature",

                        "sub_category": "Mountain / Viewpoint"

                    },


                    {

                        "name": "Ella Rock",

                        "category": "Nature",

                        "sub_category": "Mountain / Viewpoint"

                    }

                ]

            },


            {

                "destination": "Nuwara Eliya",

                "score": 0.814,

                "attractions": [

                    {

                        "name": "World's End",

                        "category": "Scenic & Leisure",

                        "sub_category": "Viewpoint"

                    }

                ]

            }

        ]

    }

}



# ==========================================
# Run Food Agent
# ==========================================

updated_state = food_agent_node(state)



# ==========================================
# Display Food Agent Result
# ==========================================

print("\n==============================")
print("FOOD AGENT OUTPUT")
print("==============================")



for destination in updated_state.get(

    "food_recommendations",

    []

):


    print(
        "\nDestination:",
        destination.get(
            "destination"
        )
    )


    print(
        "-" * 50
    )



    print(
        "\nTraveller Context:"
    )


    print(
        destination.get(
            "traveller_context"
        )
    )



    print(
        "\nDestination Context:"
    )


    print(
        destination.get(
            "destination_context"
        )
    )



    print(
        "\nRestaurants:"
    )



    for index, restaurant in enumerate(

        destination.get(
            "restaurants",
            []
        ),

        start=1

    ):


        print(
            "\nRestaurant",
            index
        )


        print(
            "Name:",
            restaurant.get(
                "restaurant_name"
            )
        )


        print(
            "City:",
            restaurant.get(
                "city"
            )
        )


        print(
            "Cuisine:",
            restaurant.get(
                "cuisine_type"
            )
        )


        print(
            "Rating:",
            restaurant.get(
                "rating"
            )
        )


        print(
            "Price:",
            restaurant.get(
                "price_level"
            )
        )


        print(
            "\nRecommended Dishes:"
        )


        dishes = restaurant.get(
            "recommended_dishes",
            []
        )


        if dishes:

            for dish in dishes:

                print(
                    " 🍛",
                    dish
                )

        else:

            print(
                " No linked dishes"
            )



        print(
            "\nWhy Recommended:"
        )


        reasons = restaurant.get(

            "reasoning",

            []

        )


        if reasons:

            for reason in reasons:

                print(
                    " ✓",
                    reason
                )

        else:

            print(
                " No reasoning available"
            )



print("\n==============================")
print("TEST COMPLETE")
print("==============================")