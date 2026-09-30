# Bandarawela Local Food Recommendation Dataset

Research / verification date: 2026-08-11

Architecture:
- food_items.csv
- food_places.csv
- food_place_dishes.csv
- social_recommendations.csv
- city_food_profile.csv
- recommendation_tags.csv
- source_registry.csv
- evaluation_queries.csv
- bandarawela_local_food_dataset.xlsx

Research policy:
- Official tourism/hotel and current public restaurant sources are preferred for factual information.
- Social media/community content is paraphrased into structured signals; full reviews/posts are not copied.
- Dynamic fields (ratings, review counts, operating hours) are point-in-time and should be refreshed before production.
- Missing dietary certification is not guessed.
- Bandarawela has a smaller dining market than Colombo/Ella, so the dataset emphasizes local authenticity, value, tea-country relevance and home-style food over raw restaurant count.

Suggested Food Agent flow:
LLM preference extraction -> IR retrieval -> diet/budget hard filters ->
ranking by food relevance + authenticity/value + tea/hill-country context + review/social evidence ->
LLM explanation with source provenance.
