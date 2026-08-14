# Sigiriya Local Food Recommendation Dataset

Research / verification date: 2026-08-11

This package follows the same architecture used for the Colombo, Ella and Mirissa local-food recommendation datasets.

## Files
- food_items.csv
- food_places.csv
- food_place_dishes.csv
- social_recommendations.csv
- city_food_profile.csv
- recommendation_tags.csv
- source_registry.csv
- evaluation_queries.csv
- sigiriya_local_food_dataset.xlsx

## Research policy
- Official tourism, hotel and cooking-class sources are preferred for factual dish/experience data.
- Current restaurant listing/review sources are used for point-in-time ranking, rating, dietary and qualitative dish signals.
- Reddit/community material is converted to paraphrased structured signals only; full posts/reviews are not copied.
- Social evidence is subjective and receives lower confidence than official sources.
- Missing dietary certifications are not guessed.
- Ratings, review counts, opening hours and price bands are dynamic snapshots.

## Sigiriya-specific modeling
- Separate village/home-style authenticity from tourist-facing popularity.
- Model cooking classes as a first-class food experience.
- Keep spice preference adjustable because traveller discussions indicate some tourist-facing food may be adapted milder.
- Scenic/lake/rock-view dining is a separate preference dimension, not a proxy for food quality.

## Suggested Food Agent pipeline
User query -> LLM preference extraction -> IR retrieval -> hard filters (diet/budget) ->
rank with dish links + authenticity + cooking-experience + scenic/family/value signals ->
LLM explanation with source provenance.

## Suggested ranking weights
30% user preference match
20% dish/place relevance
15% village/authenticity evidence
10% dietary match
10% budget/value match
10% rating/popularity quality
5% social/review evidence
