from services.food_agent.food_agent_service import (
    recommend_food_places,
)


response = recommend_food_places(
    city="Ella",
    budget="cheap",
    dietary="vegetarian",
    min_rating=4.0,
    prefer_local=True,
    limit=3,
)


print("\n========== FOOD AGENT SERVICE TEST ==========\n")

print("Success:")
print(response.get("success"))

print("\nMessage:")
print(response.get("message"))

print("\nQuery:")
print(response.get("query"))

print("\nRecommendation count:")
print(response.get("recommendation_count"))

print("\nRecommendations:")

for place in response.get("recommendations", []):

    print("\n" + "=" * 70)

    print(
        f"Restaurant: "
        f"{place.get('place_name')}"
    )

    print(
        f"Score: "
        f"{place.get('retrieval_score')}"
    )

    print("Reasons:")

    for reason in place.get(
        "match_reasons",
        []
    ):
        print(f"  ✓ {reason}")

print("\n========== END ==========")