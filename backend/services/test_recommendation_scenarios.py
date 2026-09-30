from destination.destination_recommender import recommend_destinations


TEST_SCENARIOS = {
    "Nature Traveller": [
        "hiking",
        "photography",
        "nature",
    ],

    "Beach Traveller": [
        "beach",
        "surfing",
        "swimming",
    ],

    "Culture Traveller": [
        "heritage",
        "architecture",
        "history",
    ],

    "Wildlife Traveller": [
        "wildlife",
        "bird watching",
        "photography",
    ],

    "Relaxed Scenic Traveller": [
        "scenic views",
        "nature",
        "relaxation",
    ],
}


for traveller_type, interests in TEST_SCENARIOS.items():

    print("\n" + "=" * 60)
    print(traveller_type.upper())
    print("=" * 60)

    print(f"Interests: {interests}")

    result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=3,
        debug=False,
    )

    print("\nMatched experiences:")

    for match in result["matched_experiences"]:
        print(
            f"  {match['interest']} "
            f"-> {match['experience_name']}"
        )

    if result["unmatched_interests"]:
        print(
            "\nUnmatched interests:",
            result["unmatched_interests"]
        )

    print("\nTop destinations:")

    for rank, destination in enumerate(
        result["recommended_destinations"],
        start=1,
    ):

        print(
            f"\n#{rank} "
            f"{destination['destination']} "
            f"- {destination['score']}"
        )

        for attraction in destination["attractions"]:
            print(
                f"   - {attraction['name']} "
                f"({attraction['match_score']})"
            )