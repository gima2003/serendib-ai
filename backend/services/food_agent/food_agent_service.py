from typing import Optional

from services.food_agent.retrieval_service import (
    find_food_places,
)


def recommend_food_places(
    city: str,
    budget: Optional[str] = None,
    dietary: Optional[str] = None,
    cuisine: Optional[str] = None,
    min_rating: Optional[float] = None,
    prefer_local: bool = False,
    limit: int = 5,
):
    """
    Main coordinator for the Local Food &
    Restaurant Intelligence Agent.

    For now this service:
    1. Accepts structured user preferences
    2. Calls the retrieval layer
    3. Returns structured recommendation results

    Later this service will also coordinate:
    - NLP / intent extraction
    - Groq LLM explanation
    - place photo/map enrichment
    - fallback logic
    - interaction with other agents
    """

    # --------------------------------------------------
    # 1. Basic input validation
    # --------------------------------------------------

    if not city or not city.strip():
        return {
            "success": False,
            "message": "City is required.",
            "recommendations": [],
        }

    if limit <= 0:
        limit = 5

    if limit > 20:
        limit = 20

    # --------------------------------------------------
    # 2. Retrieve + rank recommendations
    # --------------------------------------------------

    results = find_food_places(
        city=city,
        budget=budget,
        dietary=dietary,
        cuisine=cuisine,
        min_rating=min_rating,
        prefer_local=prefer_local,
        limit=limit,
    )

    # --------------------------------------------------
    # 3. Handle no-result case
    # --------------------------------------------------

    if not results:
        return {
            "success": True,
            "message": (
                "No matching food places were found "
                "for the selected preferences."
            ),
            "query": {
                "city": city,
                "budget": budget,
                "dietary": dietary,
                "cuisine": cuisine,
                "min_rating": min_rating,
                "prefer_local": prefer_local,
            },
            "recommendation_count": 0,
            "recommendations": [],
        }

    # --------------------------------------------------
    # 4. Build structured agent response
    # --------------------------------------------------

    return {
        "success": True,

        "message": (
            f"Found {len(results)} food recommendations "
            f"for {city}."
        ),

        "query": {
            "city": city,
            "budget": budget,
            "dietary": dietary,
            "cuisine": cuisine,
            "min_rating": min_rating,
            "prefer_local": prefer_local,
        },

        "recommendation_count": len(results),

        "recommendations": results,
    }