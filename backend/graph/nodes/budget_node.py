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
                # Convert to LKR (approx rate 300)
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
        profile_dict["transport_preferences"] = ["car"]
        
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
        
        # 3. Map Food — build FoodRecommendation objects with per-person cost estimate
        food_recs = []
        per_meal_estimate_lkr = 800.0  # Reasonable default per person per meal LKR
        for fo in food_options:
            if isinstance(fo, dict):
                cost = fo.get("estimated_cost_per_person_lkr") or per_meal_estimate_lkr
                food_recs.append(FoodRecommendation(estimated_cost_per_person_lkr=float(cost)))
        
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
