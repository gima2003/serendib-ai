import logging
from typing import Dict, Any

from state import TripState
from agents.planner.budget.schemas import Member1Profile, Member2Destinations, Member3FoodAcc, FoodRecommendation
from agents.planner.budget.budget_orchestrator import budget_plan

logger = logging.getLogger(__name__)

async def process_budget(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node — Agent 4 (Budget).
    Reads 'profile', 'destinations', 'food_options', 'accommodation_plan', 'route_plan'.
    Updates 'budget_plan'.
    """
    logger.info("Executing Budget Node")
    
    profile = state.get("profile")
    destinations = state.get("destinations", [])
    food_options = state.get("food_options", [])
    accommodation_plan = state.get("accommodation_plan")
    route_plan = state.get("route_plan")
    
    if not profile or not route_plan:
        logger.warning("Missing required state for budget (profile or route_plan).")
        return {}
        
    try:
        # 1. Map Profile — derive children count from travel_type and traveller_count
        from models.traveller_profile import TravelType
        total_travellers = profile.traveller_count or 1
        is_family = profile.travel_type == TravelType.family
        
        # Heuristic: family trips with >2 people likely have children
        if is_family and total_travellers > 2:
            adults = 2
            children = total_travellers - 2
        elif is_family and total_travellers == 2:
            adults = 2
            children = 0
        else:
            adults = total_travellers
            children = 0
        
        # Determine budget amount and normalize currency to LKR
        budget_amount = 0.0
        budget_currency = "LKR"
        if profile.budget:
            budget_amount = profile.budget.amount or 0.0
            raw_currency = (profile.budget.currency or "LKR").upper()
            if raw_currency in ("USD", "US$"):
                budget_amount = budget_amount * 300.0
                budget_currency = "LKR"
            elif raw_currency in ("EUR", "GBP"):
                budget_amount = budget_amount * 340.0
                budget_currency = "LKR"
            else:
                budget_currency = "LKR"
        
        profile_dict = profile.model_dump()
        profile_dict["trip_id"] = state.get("trip_id", "default_trip")
        profile_dict["travellers"] = {"adults": adults, "children": children}
        profile_dict["budget"] = {"amount": budget_amount, "currency": budget_currency}
        profile_dict["travel_style"] = profile.travel_pace.value if profile.travel_pace else "moderate"
        
        # Use real transport preferences from profile; default to mixed options if unspecified
        transport_prefs = getattr(profile, "transport_preferences", [])
        if not transport_prefs:
            raw_transport_prefs = getattr(profile, "additional_requests", [])
            for req in (raw_transport_prefs or []):
                req_lower = req.lower()
                if "car" in req_lower or "taxi" in req_lower or "private" in req_lower:
                    transport_prefs.append("car")
                elif "train" in req_lower:
                    transport_prefs.append("train")
                elif "bus" in req_lower:
                    transport_prefs.append("bus")
        
        # Default: evaluate all modes if no specific preference stated
        if not transport_prefs:
            transport_prefs = ["bus", "train", "car"]
            
        profile_dict["transport_preferences"] = list(set(transport_prefs))
        
        member1_profile = Member1Profile(**profile_dict)
        
        # 2. Map Destinations/Attractions
        mapped_destinations = []
        for d in destinations:
            city_name = d.get("city") or d.get("destination", "Unknown")
            mapped_attrs = []
            for attr in d.get("attractions", []):
                cost_val = 0.0
                # Try entry_costs array first (from destination recommender)
                entry_costs = attr.get("entry_costs", [])
                if entry_costs and isinstance(entry_costs, list) and len(entry_costs) > 0:
                    first_cost = entry_costs[0]
                    if isinstance(first_cost, dict):
                        cost_val = float(first_cost.get("price_lkr", 0) or first_cost.get("amount_lkr", 0) or 0)
                if cost_val == 0.0:
                    cost_val = float(attr.get("cost_lkr") or attr.get("estimated_entry_cost_lkr") or 0.0)
                    if cost_val == 0.0:
                        est = attr.get("cost_estimate", {})
                        if isinstance(est, dict):
                            cost_val = float(est.get("amount_lkr", 0) or 0)
                
                mapped_attrs.append({
                    "name": attr.get("name", "Unknown Attraction"),
                    "estimated_entry_cost_lkr": cost_val,
                    "cost_type": "per_person"
                })
            mapped_destinations.append({"city": city_name, "attractions": mapped_attrs})
        member2_destinations = Member2Destinations(destinations=mapped_destinations)
        
        # 3. Map Food — use actual per-person cost from food agent
        # Food cost should be meals_per_day * days * travellers
        # We estimate 2 restaurant meals/day (lunch + dinner), breakfast at accommodation
        food_recs = []
        duration_days = profile.duration_days or 1
        meals_per_day = 2  # lunch + dinner; breakfast assumed included with accommodation
        
        # Group food by city and create meal-count-aware estimates
        from collections import defaultdict
        city_foods = defaultdict(list)
        for fo in food_options:
            if isinstance(fo, dict):
                city = fo.get("city", "")
                if city:
                    city_foods[city].append(fo)
        
        # Distribute meals across days: each city gets proportional days
        num_cities = len(set(d.get("city") or d.get("destination") for d in destinations)) or 1
        days_per_city = max(1, duration_days // num_cities)
        
        for city, restaurants in city_foods.items():
            if not restaurants:
                continue
            # Estimate meals for this city
            city_meals = days_per_city * meals_per_day
            for meal_idx in range(city_meals):
                # Rotate through available restaurants
                rest = restaurants[meal_idx % len(restaurants)]
                cost = float(rest.get("estimated_cost_per_person_lkr") or 1500.0)
                food_recs.append(FoodRecommendation(estimated_cost_per_person_lkr=cost))
        
        # If no food options at all, create a reasonable estimate
        if not food_recs:
            avg_meal_cost = 1500.0 if budget_amount > 50000 else 900.0
            for _ in range(duration_days * meals_per_day):
                food_recs.append(FoodRecommendation(estimated_cost_per_person_lkr=avg_meal_cost))
        
        # 4. Map Accommodation
        acc_recs = []
        if accommodation_plan and accommodation_plan.accommodation_plan:
            for plan in accommodation_plan.accommodation_plan:
                for opt in plan.hotel_options:
                    price_per_night = 0.0
                    if opt.price_information:
                        price_per_night = (
                            opt.price_information.estimated_price_per_night_lkr
                            or opt.price_information.estimated_cost_per_night_lkr
                            or 0.0
                        )
                    if price_per_night == 0.0:
                        # Fallback estimate based on budget range
                        price_per_night = max(5000.0, budget_amount * 0.15 / max(1, len(accommodation_plan.accommodation_plan)))
                    
                    acc_recs.append({
                        "accommodation_id": opt.accommodation_id,
                        "name": opt.name,
                        "city": opt.city,
                        "estimated_cost_per_night_lkr": price_per_night,
                        "required_rooms": 1 if total_travellers <= 2 else 2,
                        "recommended_nights": plan.nights,
                        "is_selected": opt.is_selected
                    })
                     
        member3_foodacc = Member3FoodAcc(
            food_recommendations=food_recs,
            accommodation_recommendations=acc_recs
        )
        
        # Execute Budget Agent
        budget_resp = await budget_plan(
            member1_profile,
            member2_destinations,
            member3_foodacc,
            route_plan
        )
        
        logger.info(f"Budget calculated: total={budget_resp.estimated_total_cost_lkr} LKR, transport={budget_resp.cost_breakdown.transport_lkr}")
        return {"budget_plan": budget_resp}
    except Exception as e:
        logger.error(f"Error in Budget Node: {str(e)}", exc_info=True)
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Budget calculation failed: {str(e)}"]}
