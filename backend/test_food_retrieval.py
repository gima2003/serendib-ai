from services.food_agent.retrieval_service import find_places_by_city

results = find_places_by_city("Ella")

print("\n========== ELLA FOOD PLACES ==========\n")

for place in results:
    print(
        f"{place.get('place_name')} | "
        f"Rating: {place.get('rating')} | "
        f"Price: {place.get('price_band_lkr')}"
    )

print(f"\nTotal results returned: {len(results)}")