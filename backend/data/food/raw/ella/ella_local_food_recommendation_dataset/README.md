# Ella Local Food Recommendation Dataset

Research / verification date: 2026-08-11

This package mirrors the schema and research approach used in the Colombo Local Food Recommendation Dataset.

## Files
- food_items.csv
- food_places.csv
- food_place_dishes.csv
- social_recommendations.csv
- city_food_profile.csv
- recommendation_tags.csv
- source_registry.csv
- evaluation_queries.csv
- ella_local_food_dataset.xlsx

## Research approach
- Current business listings provide point-in-time ratings, review counts, hours, addresses and price bands.
- Official restaurant/experience websites and menus are preferred for cuisine and dish evidence.
- Sri Lanka Tourism is used for general Sri Lankan food definitions.
- Public Reddit, Instagram/Facebook and travel/review pages are converted into structured recommendation signals.
- Full user reviews/posts are not copied.
- Subjective claims from social media are stored only as lower-confidence qualitative signals.

## Important data-quality rules
- Missing dietary certification is not guessed.
- Ratings, review counts, price bands and hours are time-sensitive snapshots.
- "local_food_strength" is a curated retrieval feature based on cuisine positioning and evidence, not an official rating.
- Popularity does not equal authenticity. Ella has a highly tourist-oriented central restaurant scene, so the recommendation model should keep those concepts separate.
- A negative public social-media allegation is included only as a Responsible-AI/fairness risk signal and must not be treated as established fact about a venue.

## Suggested Food Agent flow
User query
-> LLM extracts city, dish, budget, dietary needs, authenticity preference, meal time
-> IR retrieves food items + food places
-> hard filters apply budget/diet constraints
-> ranking uses food-place evidence + local/authenticity signals + review/social evidence
-> LLM explains top results and cites provenance

## Suggested ranking weights
30% user preference match
20% dish/place relevance
15% local/authenticity evidence
10% dietary match
10% budget match
10% rating/popularity quality
5% social recommendation evidence

For a production application, refresh dynamic business fields and integrate live geospatial routing.
