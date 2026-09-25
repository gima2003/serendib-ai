from services.food_agent.retrieval_service import find_food_places


print("\n========== ADVANCED FOOD RETRIEVAL TEST ==========\n")

results = find_food_places(
    city="Ella",
    budget="cheap",
    dietary="vegetarian",
    min_rating=4.0,
    prefer_local=True,
    limit=5
)


if not results:
    print("❌ No matching restaurants found.")

else:
    for index, place in enumerate(results, start=1):

        print("=" * 70)
        print(f"RESULT {index}")
        print("=" * 70)

        print(f"Restaurant : {place.get('place_name')}")
        print(f"City       : {place.get('city')}")
        print(f"Area       : {place.get('area')}")
        print(f"Address    : {place.get('address')}")

        print(
            f"Rating     : "
            f"{place.get('rating')} "
            f"({place.get('review_count')} reviews)"
        )

        print(
            f"Price      : "
            f"{place.get('price_band_lkr')}"
        )

        print(
            f"Dietary    : "
            f"{place.get('dietary_strength')}"
        )

        print(
            f"Local Food : "
            f"{place.get('local_food_strength')}"
        )

        print(
            f"Score      : "
            f"{place.get('retrieval_score')}"
        )

        print("\nWhy matched:")

        for reason in place.get(
            "match_reasons", []
        ):
            print(f"  ✓ {reason}")

        print("\nRecommended / linked dishes:")

        dishes = place.get("dishes", [])

        if dishes:

            for dish in dishes[:5]:
                print(
                    f"  🍛 "
                    f"{dish.get('food_name')}"
                )

        else:
            print(
                "  ℹ️ No linked dish records available"
            )

        print("\nCommunity signals:")

        signals = place.get(
            "social_signals", []
        )

        if signals:

            for signal in signals:

                print(
                    f"  💬 "
                    f"{signal.get('structured_summary')}"
                )

        else:
            print(
                "  ℹ️ No linked social signals available"
            )

        print(
            f"\nMap query  : "
            f"{place.get('map_query')}"
        )

        print(
            f"Photo URL  : "
            f"{place.get('photo_url')}"
        )

        print()


print("=" * 70)
print(f"Total matching results: {len(results)}")
print("=" * 70)