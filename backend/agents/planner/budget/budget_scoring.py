from typing import List, Optional
from agents.planner.budget.schemas import TransportOption, RecommendedTransport

def recommend_transport(
    transport_options: List[TransportOption],
    preferences: List[str],
    remaining_budget_for_transport: float
) -> RecommendedTransport:
    """
    Selects the best transport mode based on:
    1. Valid pricing/data
    2. Affordability
    3. Traveller transport preference
    4. Cost efficiency
    """
    valid_options = [opt for opt in transport_options if opt.price_available and opt.coverage == "complete"]
    
    if not valid_options:
        return RecommendedTransport(
            recommended_mode="unknown",
            estimated_cost_lkr=0.0,
            reason=["No valid transport options with verifiable pricing could be calculated from the datasets."]
        )
        
    # Scoring
    best_score = -9999
    best_opt = None
    
    for opt in valid_options:
        score = 0
        
        # Affordability
        if opt.estimated_cost_lkr <= remaining_budget_for_transport:
            score += 50
        else:
            score -= 50 # Over budget penalty
            
        # Preference Match
        if opt.mode.lower() in [p.lower() for p in preferences]:
            score += 30
            
        # Efficiency (Cheaper is slightly better if all else equal)
        # Using negative cost scaled down so cheaper options get a small boost
        score -= (opt.estimated_cost_lkr / 10000)
        
        if score > best_score:
            best_score = score
            best_opt = opt
            
    if best_opt:
        reasons = []
        if best_opt.estimated_cost_lkr <= remaining_budget_for_transport:
            reasons.append("Fits within the available trip budget.")
        else:
            reasons.append("Exceeds available budget but is the best available option.")
            
        if best_opt.mode.lower() in [p.lower() for p in preferences]:
            reasons.append("Matches traveller transport preference.")
            
        reasons.append(f"Estimated cost: {best_opt.estimated_cost_lkr} LKR.")
        
        return RecommendedTransport(
            recommended_mode=best_opt.mode,
            estimated_cost_lkr=best_opt.estimated_cost_lkr,
            reason=reasons
        )
        
    return RecommendedTransport(
        recommended_mode="unknown",
        estimated_cost_lkr=0.0,
        reason=["Could not determine a recommendation based on available options."]
    )
