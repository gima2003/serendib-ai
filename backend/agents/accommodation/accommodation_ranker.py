from typing import List
from agents.accommodation.schemas import AccommodationCandidate, AccommodationRecommendationResult

def rank_accommodations(
    candidates: List[AccommodationCandidate],
    travel_type: str,
    travel_pace: str,
    interests: List[str],
    daily_budget_estimate: float
) -> List[AccommodationRecommendationResult]:
    """
    Deterministically ranks accommodation candidates based on preferences and estimated budget.
    """
    results = []
    
    for candidate in candidates:
        score = 50.0 # Base score
        reasons = []
        
        acc_type = candidate.accommodation_type.lower()
        
        # Match by travel type
        if travel_type == "couple":
            if "boutique" in acc_type or "villa" in acc_type or "resort" in acc_type:
                score += 20
                reasons.append("Suitable for couple travellers")
        elif travel_type == "solo":
            if "hostel" in acc_type or "guest" in acc_type:
                score += 20
                reasons.append("Great for solo travellers")
                
        # Match by interests
        if "nature" in interests:
            if "eco" in acc_type or "lodge" in acc_type:
                score += 15
                reasons.append("Matches nature preference")
                
        # Rating boost
        if candidate.rating:
            if candidate.rating >= 4.5:
                score += 15
                reasons.append("Excellent guest rating")
            elif candidate.rating >= 4.0:
                score += 10
                reasons.append("Good guest rating")
                
        # Budget check
        price = candidate.price_information.estimated_price_per_night_lkr
        if price:
            if price <= daily_budget_estimate:
                score += 15
                reasons.append("Within estimated budget range")
            else:
                score -= 10
                reasons.append("Slightly above estimated budget")
                
        # Create result
        result_dict = candidate.model_dump()
        result = AccommodationRecommendationResult(
            **result_dict,
            recommendation_score=score,
            recommendation_reasons=reasons
        )
        results.append(result)
        
    # Sort descending by score
    results.sort(key=lambda x: x.recommendation_score, reverse=True)
    return results
