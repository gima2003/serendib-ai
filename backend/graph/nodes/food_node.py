import logging
import re
from typing import Dict, Any, List

from state import TripState
from services.food_agent.food_agent_service import recommend_food_places

logger = logging.getLogger(__name__)


def _parse_price_band(price_band: str, budget_level: str) -> float:
    """
    Convert unstructured price_band_lkr strings like 'Rs 1,000–2,000' or 'Budget signal'
    into a numeric midpoint estimate per person in LKR.
    Falls back to budget-level defaults if parsing fails.
    """
    if not price_band:
        defaults = {"budget": 900.0, "moderate": 1800.0, "upscale": 4000.0}
        return defaults.get(budget_level, 1500.0)
    
    cleaned = str(price_band).replace(",", "").replace("Rs", "").replace("LKR", "").strip()
    
    # Extract all numbers in the string
    numbers = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', cleaned)]
    
    if len(numbers) >= 2:
        # Range like 1000–2000 → midpoint
        return round((numbers[0] + numbers[1]) / 2.0, 0)
    elif len(numbers) == 1:
        return numbers[0]
    
    # Keyword fallback
    lower = cleaned.lower()
    if any(w in lower for w in ["budget", "cheap", "low", "affordable"]):
        return 900.0
    elif any(w in lower for w in ["mid", "medium", "moderate"]):
        return 1800.0
    elif any(w in lower for w in ["high", "premium", "luxury", "expensive"]):
        return 4000.0
    
    defaults = {"budget": 900.0, "moderate": 1800.0, "upscale": 4000.0}
    return defaults.get(budget_level, 1500.0)


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
        
        # Extract ALL dietary requirements (not just the first)
        dietary = None
        if profile.dietary_requirements:
            dietary = profile.dietary_requirements[0]  # Primary requirement for filtering
            
        # Extract food preferences
        prefer_local = "local_food" in (profile.food_preferences or [])
        
        # Budget level — consider total budget vs. trip length and travellers
        budget_level = "moderate"
        travellers = profile.traveller_count or 1
        duration = profile.duration_days or 1
        if profile.budget and profile.budget.amount:
            amount = profile.budget.amount
            currency = (profile.budget.currency or "LKR").upper()
            if currency != "LKR":
                amount = amount * 300
            # Per-person per-day budget for food (estimated ~15% of total budget)
            food_budget_per_person_per_day = (amount * 0.15) / max(1, travellers) / max(1, duration)
            if food_budget_per_person_per_day < 1000:
                budget_level = "budget"
            elif food_budget_per_person_per_day > 3000:
                budget_level = "upscale"
            else:
                budget_level = "moderate"
            
        food_recommendations = []
        for city in cities:
            res = recommend_food_places(
                city=city,
                budget=budget_level,
                dietary=dietary,
                prefer_local=prefer_local,
                limit=4  # Up from 3 to have dinner+lunch options per day
            )
            if res and res.get("recommendations"):
                for r in res["recommendations"]:
                    # Parse actual price from price_band_lkr field returned by retrieval service
                    price_band = r.get("price_band_lkr", "")
                    estimated_cost = _parse_price_band(price_band, budget_level)
                    
                    # Build reasoning from match_reasons (actual field from retrieval service)
                    reasons = r.get("match_reasons", [])
                    reasoning = "; ".join(reasons) if reasons else f"Recommended for {city}"
                    
                    # dietary_info from dietary_strength (actual field from retrieval service)
                    dietary_info = []
                    dietary_strength = r.get("dietary_strength", "")
                    if dietary_strength:
                        dietary_info = [dietary_strength]
                    
                    food_recommendations.append({
                        "city": city,
                        "place_name": r.get("place_name", "Local Restaurant"),
                        "estimated_cost_per_person_lkr": estimated_cost,
                        "price_band_lkr": price_band,
                        "reasoning": reasoning,
                        "cuisine_type": r.get("cuisine_focus", r.get("cuisine_type", "Local")),
                        "dietary_accommodations": dietary_info,
                        "rating": r.get("rating"),
                        "address": r.get("address", ""),
                        "opening_hours": r.get("opening_hours", ""),
                        "signature_dishes": r.get("signature_dishes", []),
                    })
                    
        logger.info(f"Food recommendations: {len(food_recommendations)} items across {len(cities)} cities")
        return {"food_options": food_recommendations}
    except Exception as e:
        logger.error(f"Error in Food Node: {str(e)}", exc_info=True)
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Food recommendation failed: {str(e)}"]}
