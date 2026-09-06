from destination.destination_recommender import (
    recommend_from_traveller_profile
)


# Simulated structured output from Agent 1
traveller_profile = {
    "budget": {
        "amount": 700,
        "currency": "USD",
    },

    "duration_days": 6,

    "traveller_count": 2,

    "travel_type": "couple",

    "interests": [
        "beach",
        "nature",
        "photography",
    ],

    "dietary_requirements": [
        "vegetarian"
    ],

    "preferences": {
        "crowd_preference": "low",
        "travel_pace": "moderate",
    },

    "preferred_destinations": [],

    "accessibility_requirements": [],
}


result = recommend_from_traveller_profile(
    traveller_profile=traveller_profile,
    top_destinations=5,
    top_attractions=3,
    debug=False,
)


print("\n==========================================")
print("AGENT 1 -> AGENT 2 CONTRACT TEST")
print("==========================================")

print("\nAgent 2 received:")
print(result["agent2_input"])

print("\nMatched experiences:")

for item in result["matched_experiences"]:
    print(
        f"- {item['interest']} "
        f"-> {item['experience_name']}"
    )


print("\nRecommended destinations:")

for rank, destination in enumerate(
    result["recommended_destinations"],
    start=1,
):

    print(
        f"\n#{rank} "
        f"{destination['destination']} "
        f"- Score: {destination['score']}"
    )

    print(
        f"Interest coverage: "
        f"{destination['interest_coverage']}"
    )

    for attraction in destination["attractions"]:

        print(
            f"  - {attraction['name']} "
            f"({attraction['match_score']})"
        )