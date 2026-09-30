from destination.destination_recommender import recommend_destinations


result = recommend_destinations(
    interests=[
        "hiking",
        "photography",
        "nature",
    ],
    top_destinations=5,
    top_attractions=5,
    debug=True
)


print("\n==========================================")
print("AGENT 2 - RECOMMENDER TEST")
print("==========================================")

print("\nMatched experiences:")

for item in result["matched_experiences"]:
    print(
        f"- {item['interest']} "
        f"-> {item['experience_name']}"
    )


print("\nRecommended destinations:")

for rank, destination in enumerate(
    result["recommended_destinations"],
    start=1
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

    print(
        f"Strong attractions: "
        f"{destination['strong_attractions']}"
    )

    print("Attractions:")

    for attraction in destination["attractions"]:

        print(
            f"  - {attraction['name']} "
            f"({attraction['match_score']})"
        )