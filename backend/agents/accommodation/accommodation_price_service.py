from agents.accommodation.schemas import AccommodationCandidate, AccommodationPriceInfo

# Simple reference based on the project instructions (USD converted to LKR roughly, 1 USD = ~300 LKR)
# Budget / 3-star: 41-47 USD -> ~ 12300 - 14100 LKR
# 4-star: 63-79 USD -> ~ 18900 - 23700 LKR
# 5-star / luxury: 109-154 USD -> ~ 32700 - 46200 LKR
# Guesthouses/Hostels: Usually lower, maybe 5000 - 10000 LKR

def estimate_accommodation_price(candidate: AccommodationCandidate, budget_amount: float) -> AccommodationCandidate:
    """
    Estimates the nightly price for an accommodation if it doesn't have one.
    """
    # If a real source already provided a price, preserve it.
    if candidate.price_information and candidate.price_information.type == "source_provided":
        if candidate.price_information.min_per_night_lkr and candidate.price_information.max_per_night_lkr:
            mid = (candidate.price_information.min_per_night_lkr + candidate.price_information.max_per_night_lkr) / 2
            candidate.price_information.estimated_price_per_night_lkr = mid
        return candidate
        
    acc_type = candidate.accommodation_type.lower()
    
    # Very basic heuristic for estimation based on type
    if "resort" in acc_type or "villa" in acc_type:
        min_p, max_p = 20000, 35000
    elif "hotel" in acc_type:
        min_p, max_p = 12000, 20000
    elif "guest" in acc_type or "hostel" in acc_type:
        min_p, max_p = 5000, 10000
    else:
        min_p, max_p = 8000, 15000
        
    # We could adjust based on Google Places rating if available
    if candidate.rating and candidate.rating > 4.5:
        min_p = int(min_p * 1.5)
        max_p = int(max_p * 1.5)
        
    midpoint = (min_p + max_p) / 2
    
    candidate.price_information = AccommodationPriceInfo(
        type="estimated_range",
        min_per_night_lkr=float(min_p),
        max_per_night_lkr=float(max_p),
        estimated_price_per_night_lkr=float(midpoint),
        price_basis="room",
        source="estimated_accommodation_reference",
        confidence="medium"
    )
    
    return candidate
