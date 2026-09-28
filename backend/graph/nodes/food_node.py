import logging
from typing import Dict, Any, List

from state import TripState
from services.food_agent.food_agent_service import recommend_food_places

logger = logging.getLogger(__name__)

async def process_food(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node — Agent 3 (Food).
    Reads 'destinations' and 'profile' from state and updates 'food_options'.
    """
    logger.info("Executing Food Node")
    
    destinations = state.get("destinations", [])
    profile = state.get("profile")
    
    if not destinations or not profile:
        logger.warning("Missing destinations or profile, skipping food recommendation.")
        return {}
        
    try:
        cities: List[str] = []
        for d in destinations:
            city = d.get("city") or d.get("destination")
            if city and city not in cities:
                cities.append(city)
        
        # Extract dietary preferences
        dietary = None
        if profile.dietary_requirements:
            dietary = profile.dietary_requirements[0]  # Use primary dietary requirement
            
        # Extract food preferences
        prefer_local = "local_food" in (profile.food_preferences or [])
        
        # Budget level
        budget_level = "moderate"
        if profile.budget and profile.budget.amount:
            # Rough categorisation: < 20000 LKR budget = budget, > 100000 = upscale
            amount = profile.budget.amount
            currency = (profile.budget.currency or "LKR").upper()
            if currency != "LKR":
                amount = amount * 300
            if amount < 30000:
                budget_level = "budget"
            elif amount > 150000:
                budget_level = "upscale"
            
        food_recommendations = []
        for city in cities:
            res = recommend_food_places(
                city=city,
                budget=budget_level,
                dietary=dietary,
                prefer_local=prefer_local,
                limit=3
            )
            if res and res.get("recommendations"):
                for r in res["recommendations"]:
                    food_recommendations.append({
                        "city": city,
                        "place_name": r.get("place_name", "Local Restaurant"),
                        "estimated_cost_per_person_lkr": float(r.get("estimated_cost_per_person_lkr") or 800.0),
                        "reasoning": r.get("reasoning", ""),
                        "cuisine_type": r.get("cuisine_focus", r.get("cuisine_type", "Local")),
                        "dietary_accommodations": r.get("dietary_info", []),
                        "rating": r.get("rating"),
                        "address": r.get("address", ""),
                    })
                    
        logger.info(f"Food recommendations: {len(food_recommendations)} items across {len(cities)} cities")
        return {"food_options": food_recommendations}
    except Exception as e:
        logger.error(f"Error in Food Node: {str(e)}", exc_info=True)
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Food recommendation failed: {str(e)}"]}
