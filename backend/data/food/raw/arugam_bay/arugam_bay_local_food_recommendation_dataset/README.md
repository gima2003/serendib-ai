# Arugam Bay Local Food Recommendation Dataset

Research / verification date: 2026-08-11

This package follows the same architecture used for the Colombo, Ella, Mirissa, Sigiriya and Bandarawela food datasets.

Files:
- food_items.csv
- food_places.csv
- food_place_dishes.csv
- social_recommendations.csv
- city_food_profile.csv
- recommendation_tags.csv
- source_registry.csv
- evaluation_queries.csv
- arugam_bay_local_food_dataset.xlsx

Research policy:
- Official tourism/restaurant/cooking-class sources are preferred for factual information.
- Current business listings and review aggregators are used for point-in-time ratings, review counts, hours and dish/aspect signals.
- Reddit/community/travel-blog content is paraphrased into structured signals; full posts/reviews are not copied.
- Social evidence is subjective and assigned lower confidence.
- Missing dietary certification is not guessed.
- Dynamic hours/prices/review counts should be refreshed before production deployment.

Arugam Bay-specific modeling:
- Separate fresh-catch quality, local authenticity, tourist popularity and beach/social atmosphere.
- Include Tamil/South-Indian food as a meaningful regional option.
- Treat cooking classes as a first-class local-food experience.
- Keep spice preference explicit because community discussions indicate some tourist-facing food may be milder.

Suggested Food Agent pipeline:
LLM preference extraction -> IR retrieval -> hard filters (diet/budget/time) ->
ranking using food-place links + fresh-catch/authenticity + social evidence ->
LLM explanation with source provenance.
