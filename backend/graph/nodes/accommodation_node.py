import logging
from typing import Dict, Any

from state import TripState
from agents.accommodation.schemas import AccommodationRequest, StayRequest, BudgetRequest
from agents.accommodation.accommodation_service import process_accommodation_request

logger = logging.getLogger(__name__)

async def process_accommodation(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node that acts as a thin wrapper around Agent 3 (Accommodation).
    Reads 'profile' and 'destinations' from state and updates 'accommodation_plan' and 'stays'.
    """
    logger.info("Executing Accommodation Node")
    
    profile = state.get("profile")
    destinations = state.get("destinations", [])
    
    if not profile or not destinations:
        logger.warning("Missing profile or destinations, skipping accommodation.")
        return {}
        
    try:
        cities = [d.get("city") or d.get("destination") for d in destinations if d.get("city") or d.get("destination")]
        
        # Calculate nights per city evenly (as in integration test)
        total_days = profile.duration_days or len(cities)
        days_per_city = max(1, total_days // max(1, len(cities)))
        
        stays = [StayRequest(city=c, nights=days_per_city) for c in cities]
        
        budget_req = None
        if profile.budget:
            budget_req = BudgetRequest(
                amount=profile.budget.amount or 0.0,
                currency=profile.budget.currency or "USD"
            )
        else:
            budget_req = BudgetRequest(amount=1000.0, currency="USD")
            
        acc_req = AccommodationRequest(
            traveller_count=profile.traveller_count or 1,
            travel_type=profile.travel_type.value if profile.travel_type else "solo",
            travel_pace=profile.travel_pace.value if profile.travel_pace else "balanced",
            interests=[i.name for i in profile.interests] if profile.interests else [],
            budget=budget_req,
            stays=stays
        )
        
        acc_response = process_accommodation_request(acc_req)
        
        # Also store 'stays' for downstream (Schedule Agent needs acc_response.accommodation_plan)
        return {
            "accommodation_plan": acc_response,
            "stays": acc_response.accommodation_plan
        }
    except Exception as e:
        logger.error(f"Error in Accommodation Node: {str(e)}")
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Accommodation recommendation failed: {str(e)}"]}
