from models.traveller_profile import TravellerProfile
from services.profile_normalizer import normalize_traveller_profile


profile = TravellerProfile(
    duration_days=6,
    traveller_count=2,
    travel_type="couple",

    budget={
        "amount": 700,
        "currency": "usd",
        "scope": "total_trip",
        "flexibility": None,
    },

    interests=[
        {
            "name": "quiet coastal villages with photography",
            "preference": "high",
        }
    ],

    dietary_requirements=[
        "veg",
        "gluten-free",
    ],

    additional_requests=[
        "avoid rushed travel and spend time with locals"
    ],
)


normalized_profile = normalize_traveller_profile(profile)


print(
    normalized_profile.model_dump_json(
        indent=2
    )
)