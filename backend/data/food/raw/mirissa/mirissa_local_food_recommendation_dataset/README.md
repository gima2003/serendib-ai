# Mirissa Local Food Recommendation Dataset

Research / verification date: 2026-08-11

This package follows the same architecture used for the Colombo and Ella local-food datasets.

## Files
- food_items.csv
- food_places.csv
- food_place_dishes.csv
- social_recommendations.csv
- city_food_profile.csv
- recommendation_tags.csv
- source_registry.csv
- evaluation_queries.csv
- mirissa_local_food_dataset.xlsx

## Research policy
- Official restaurant/tourism sources are preferred for factual identity and dish information.
- Current review aggregators provide point-in-time ratings and qualitative dish/aspect signals.
- Reddit/Instagram/Facebook content is transformed into structured, paraphrased signals; full posts/reviews are not copied.
- Social and review signals are subjective and receive lower confidence than official sources.
- Missing dietary certifications are not guessed.
- Ratings, review counts, opening hours and price bands are time-sensitive snapshots.
- Mirissa has a strong tourist-facing beach restaurant scene; tourist popularity and local authenticity are deliberately stored as separate concepts.

## Recommended Food Agent flow
User query -> LLM preference extraction -> IR retrieval -> hard filters (diet/budget) ->
rank using dish links + authenticity/locality + price + rating/popularity + social evidence ->
LLM explanation with source provenance.

## Suggested ranking weights
30% preference match
20% dish/place relevance
15% local/authenticity evidence
10% dietary match
10% budget match
10% rating/popularity quality
5% social recommendation evidence
