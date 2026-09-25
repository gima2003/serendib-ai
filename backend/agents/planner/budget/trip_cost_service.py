from agents.planner.budget.schemas import Member1Profile, Member2Destinations, Member3FoodAcc
from agents.planner.budget.schemas import CostBreakdown

def calculate_trip_costs(
    profile: Member1Profile,
    destinations: Member2Destinations,
    food_acc: Member3FoodAcc
) -> tuple[float, float, float]:
    """
    Calculates the non-transport costs of the trip.
    Returns: (accommodation_lkr, food_lkr, attractions_lkr)
    """
    total_travellers = profile.travellers.adults + profile.travellers.children
    
    # 1. Food Cost
    # Schema defines estimated_cost_per_person_lkr for each meal
    food_lkr = 0.0
    for meal in food_acc.food_recommendations:
        food_lkr += meal.estimated_cost_per_person_lkr * total_travellers
        
    # 2. Accommodation Cost
    # Schema defines estimated_cost_per_night_lkr and recommended_nights
    # We do NOT multiply by total_travellers because accommodation pricing is typically per room/unit
    # unless specified as per person.
    acc_lkr = 0.0
    for acc in food_acc.accommodation_recommendations:
        acc_lkr += acc.estimated_cost_per_night_lkr * acc.recommended_nights
        
    # 3. Attraction Cost
    # Schema defines estimated_entry_cost_lkr. 
    # It does not explicitly define it as 'per_person', so we adhere strictly to the schema 
    # and treat it as the total cost to avoid inventing a multiplier not supported by the schema.
    attr_lkr = 0.0
    for dest in destinations.destinations:
        for attr in dest.attractions:
            attr_lkr += attr.estimated_entry_cost_lkr
            
    return acc_lkr, food_lkr, attr_lkr
