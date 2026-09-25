# Colombo Local Food Recommendation Dataset

Research date: 2026-08-11

This is a curated, research-grounded prototype dataset for a Local Food Recommendation Agent.

## Included files
- food_items.csv
- food_places.csv
- food_place_dishes.csv
- social_recommendations.csv
- city_food_profile.csv
- recommendation_tags.csv
- source_registry.csv
- evaluation_queries.csv
- colombo_local_food_dataset.xlsx

## Data policy
- Official tourism/restaurant sources are preferred for factual information.
- Social-media/forum posts are converted to structured, paraphrased recommendation signals; full posts/reviews are not copied.
- Social evidence is subjective and assigned lower confidence.
- Missing dietary certifications are not guessed.
- Current ratings, review counts, hours and price bands are time-sensitive snapshots.
- This is a curated Colombo prototype, not an exhaustive list of all restaurants.

## Suggested Local Food Agent flow
User query -> LLM preference extraction -> retrieve food/place candidates ->
hard-filter dietary and budget constraints -> rank with place-dish and social signals ->
LLM explains the top matches with provenance.

## Suggested ranking
30% preference match
20% dish/place relevance
15% local/authenticity signal
10% dietary match
10% budget match
10% rating quality
5% social recommendation evidence
