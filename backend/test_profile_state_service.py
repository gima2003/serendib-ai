from models.traveller_profile import TravellerProfile

from services.profile_state_service import (
    create_profile_state,
)


ready_profile = TravellerProfile(
    duration_days=6,
    traveller_count=2,
    travel_type="couple",

    interests=[
        {
            "name": "beach",
            "preference": "high",
        }
    ],

    food_preferences=[
        "local_food"
    ],

    travel_pace="relaxed",
)


incomplete_profile = TravellerProfile(
    traveller_count=2,
    travel_type="couple",

    interests=[
        {
            "name": "beach",
            "preference": "high",
        }
    ],
)


print("READY PROFILE STATE")

ready_state = create_profile_state(
    ready_profile
)

print(
    ready_state.model_dump_json(
        indent=2
    )
)


print("\nINCOMPLETE PROFILE STATE")

incomplete_state = create_profile_state(
    incomplete_profile
)

print(
    incomplete_state.model_dump_json(
        indent=2
    )
)