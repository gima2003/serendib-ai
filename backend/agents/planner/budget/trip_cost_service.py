from agents.planner.budget.schemas import Member1Profile, Member2Destinations, Member3FoodAcc
from agents.planner.budget.schemas import CostBreakdown

def calculate_trip_costs(
    profile: Member1Profile,
    destinations: Member2Destinations,
    food_acc: Member3FoodAcc
) -> tuple[float, float, float, list[str]]:
    """
    Calculates the non-transport costs of the trip.
    Returns: (accommodation_lkr, food_lkr, attractions_lkr, warnings)
    """
    total_travellers = profile.travellers.adults + profile.travellers.children
    warnings = []
    
    # 1. Food Cost
    # Schema defines estimated_cost_per_person_lkr for each meal
    food_lkr = 0.0
    for meal in food_acc.food_recommendations:
        food_lkr += meal.estimated_cost_per_person_lkr * total_travellers
        
    # 2. Accommodation Cost
    acc_lkr = 0.0
    for acc in food_acc.accommodation_recommendations:
        if acc.is_selected:
            if acc.required_rooms is not None:
                acc_lkr += acc.estimated_cost_per_night_lkr * acc.required_rooms * acc.recommended_nights
            else:
                acc_lkr += acc.estimated_cost_per_night_lkr * acc.recommended_nights
                warnings.append(f"Room requirement not provided for accommodation {acc.name or 'unknown'}. Cost assumed as complete group accommodation price.")
        
    # 3. Attraction Cost
    attr_lkr = 0.0
    for dest in destinations.destinations:
        for attr in dest.attractions:
            if attr.cost_type == "per_person":
                attr_lkr += attr.estimated_entry_cost_lkr * total_travellers
            elif attr.cost_type == "flat_rate":
                attr_lkr += attr.estimated_entry_cost_lkr
            else:
                attr_lkr += attr.estimated_entry_cost_lkr
                warnings.append(f"Attraction cost type unknown for '{attr.name}'. Cost assumed as flat rate.")
            
    return acc_lkr, food_lkr, attr_lkr, warnings
