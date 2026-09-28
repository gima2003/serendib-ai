from typing import List, Optional
from agents.planner.budget.schemas import TransportOption, SavingsOpportunity, Member3FoodAcc

def find_savings_opportunities(
    selected_transport: Optional[TransportOption],
    transport_options: List[TransportOption],
    estimated_total_cost_lkr: float,
    available_budget_lkr: float,
    acc_lkr: float,
    food_lkr: float,
    attr_lkr: float,
    food_acc: Optional[Member3FoodAcc] = None
) -> tuple[List[SavingsOpportunity], float, Optional[str], Optional[float]]:
    """
    Identifies realistic savings if the trip is over budget.
    Returns: (savings, over_budget_amount, highest_expense_category, highest_expense_percentage)
    """
    savings = []
    
    if estimated_total_cost_lkr <= available_budget_lkr:
        return savings, 0.0, None, None
        
    over_budget_amount = estimated_total_cost_lkr - available_budget_lkr
    
    transport_lkr = selected_transport.estimated_cost_lkr if (selected_transport and selected_transport.price_available) else 0.0
    
    categories = {
        "Transport": transport_lkr,
        "Accommodation": acc_lkr,
        "Food": food_lkr,
        "Attractions": attr_lkr
    }
    
    highest_cost_category = max(categories, key=categories.get)
    highest_expense_percentage = (categories[highest_cost_category] / estimated_total_cost_lkr) * 100 if estimated_total_cost_lkr > 0 else 0
    
    # Accommodation savings logic
    found_acc_saving = False
    if food_acc and food_acc.accommodation_recommendations:
        # Group by city/destination (assuming the alternatives belong to the same destination)
        # We need to find if there is a cheaper alternative than the selected one for a destination
        selected_accs = [a for a in food_acc.accommodation_recommendations if a.is_selected]
        alt_accs = [a for a in food_acc.accommodation_recommendations if not a.is_selected]
        
        for selected in selected_accs:
            city_alts = [a for a in alt_accs if a.city == selected.city]
            for alt in city_alts:
                current_cost = selected.estimated_cost_per_night_lkr * selected.recommended_nights * (selected.required_rooms or 1)
                alt_cost = alt.estimated_cost_per_night_lkr * alt.recommended_nights * (alt.required_rooms or 1)
                if alt_cost < current_cost:
                    saving_lkr = current_cost - alt_cost
                    savings.append(
                        SavingsOpportunity(
                            category="Accommodation",
                            description=f"Switching from {selected.name or 'selected accommodation'} to {alt.name or 'alternative'} in {selected.city} could save money.",
                            potential_saving_lkr=saving_lkr,
                            alternative_option=alt.name or "Cheaper alternative"
                        )
                    )
                    found_acc_saving = True

    # Generic suggestions for non-transport categories if they are the highest expense
    if highest_cost_category == "Accommodation" and acc_lkr > 0 and not found_acc_saving:
        savings.append(
            SavingsOpportunity(
                category="Accommodation",
                description="Consider lower price accommodation options.",
                potential_saving_lkr=acc_lkr * 0.30, # Heuristic 30% saving
                alternative_option="Choose budget accommodation"
            )
        )
    elif highest_cost_category == "Food" and food_lkr > 0:
        savings.append(
            SavingsOpportunity(
                category="Food",
                description="Consider budget dining or self-catering options.",
                potential_saving_lkr=food_lkr * 0.20,
                alternative_option="Choose budget dining"
            )
        )
    elif highest_cost_category == "Attractions" and attr_lkr > 0:
        savings.append(
            SavingsOpportunity(
                category="Attractions",
                description="Consider removing premium attractions or finding free alternatives.",
                potential_saving_lkr=attr_lkr * 0.20,
                alternative_option="Reduce paid attractions"
            )
        )

    # Transport savings logic
    if selected_transport and selected_transport.price_available:
        current_transport_cost = selected_transport.estimated_cost_lkr
        
        valid_options = [opt for opt in transport_options if opt.price_available and opt.coverage == "complete"]
        for opt in valid_options:
            if opt.estimated_cost_lkr < current_transport_cost:
                saving_lkr = current_transport_cost - opt.estimated_cost_lkr
                savings.append(
                    SavingsOpportunity(
                        category="Transport",
                        description=f"Switching from {selected_transport.mode} to {opt.mode} can save money.",
                        potential_saving_lkr=saving_lkr,
                        alternative_option=opt.mode
                    )
                )
                
    savings.sort(key=lambda x: x.potential_saving_lkr, reverse=True)
    return savings, over_budget_amount, highest_cost_category, highest_expense_percentage
