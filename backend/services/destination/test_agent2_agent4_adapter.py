from services.destination.agent4_adapter import (
    prepare_agent4_input
)

from services.destination.destination_recommender import (
    recommend_from_traveller_profile
)


profile = {
    "profile": {
        "duration_days": 6,

        "interests": [
            {
                "name": "beach",
                "preference": "high"
            },
            {
                "name": "nature",
                "preference": "high"
            }
        ],

        "preferred_destinations": [
            "Ella"
        ],

        "crowd_preference": "avoid",

        "travel_pace": "relaxed",

        "accessibility_requirements": []
    }
}


result = recommend_from_traveller_profile(
    profile
)


agent4_input = prepare_agent4_input(
    result
)


print("==============================")
print("AGENT 2 -> AGENT 4 ADAPTER TEST")
print("==============================")

print(agent4_input)