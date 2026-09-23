from typing import List
from agents.planner.budget.schemas import TransportOption, SavingsOpportunity

def find_savings_opportunities(
    selected_transport: TransportOption,
    transport_options: List[TransportOption],
    estimated_total_cost_lkr: float,
    available_budget_lkr: float
) -> List[SavingsOpportunity]:
    """
    Identifies realistic savings if the trip is over budget.
    Only recommends alternatives supported by actual available data.
    """
    savings = []
    
    if estimated_total_cost_lkr <= available_budget_lkr:
        # Not over budget, no immediate savings required (though could provide optimization later)
        return savings
        
    # Find cheaper valid transport options
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
                
    # We do NOT automatically remove attractions, meals, or accommodation here per project rules.
    # Those decisions are handled by the complete Smart Trip Planner/replanning workflow.
    
    # Sort by highest potential savings
    savings.sort(key=lambda x: x.potential_saving_lkr, reverse=True)
    return savings
