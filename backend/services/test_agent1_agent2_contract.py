from destination.destination_recommender import (
    recommend_from_traveller_profile
)


print("=" * 60)
print("AGENT 1 -> AGENT 2 CONTRACT TEST")
print("=" * 60)


# Real Agent 1 output example

agent1_state = {

    "status": "ready",

    "profile": {

        "duration_days": 6,

        "traveller_count": 2,

        "travel_type": "couple",

        "starting_location": "Colombo",


        "budget": {
            "amount": 900,
            "currency": "USD",
            "scope": "total_trip",
            "flexibility": None
        },


        "interests": [
            {
                "name": "beach",
                "preference": "high"
            },
            {
                "name": "nature",
                "preference": "high"
            },
            {
                "name": "photography",
                "preference": "high"
            },
            {
                "name": "culture",
                "preference": "high"
            }
        ],


        "dietary_requirements": [
            "vegetarian"
        ],


        "food_preferences": [
            "local_food"
        ],


        "travel_pace": "relaxed",


        "crowd_preference": "avoid",


        "preferred_destinations": [
            "Ella",
            "southern coast"
        ],


        "must_visit_destinations": [],


        "avoidances": [
            "long road journeys",
            "crowded tourist areas"
        ],


        "accessibility_requirements": [],


        "additional_requests": [
            "Want to try authentic Sri Lankan local dishes"
        ]
    }
}



result = recommend_from_traveller_profile(
    agent1_state["profile"],
    top_destinations=5,
    top_attractions=3,
    debug=False
)



print("\nAgent 2 received:")
print("------------------------------")

print(
    result["agent2_input"]
)



print("\nRecommended Destinations:")
print("------------------------------")


for i, destination in enumerate(
    result["recommended_destinations"],
    start=1
):

    print(
        f"\n#{i} "
        f"{destination['destination']} "
        f"Score: {destination['score']}"
    )


    for attraction in destination["attractions"]:

        print(
            f"  - {attraction['name']}"
        )

        print(
            f"    Type: {attraction.get('indoor_outdoor')}"
        )


        print(
            "    Entry costs:"
        )


        for cost in attraction["entry_costs"]:

            print(
                f"      {cost}"
            )