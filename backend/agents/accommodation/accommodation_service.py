import logging
from typing import List, Dict

from agents.accommodation.schemas import (
    AccommodationRequest,
    AccommodationResponse,
    DestinationAccommodation,
    AccommodationCandidate
)
from agents.accommodation.geoapify_service import fetch_accommodations_geoapify
from agents.accommodation.osm_service import fetch_accommodations_osm
from agents.accommodation.google_places_service import enrich_accommodations_google_places
from agents.accommodation.accommodation_price_service import estimate_accommodation_price
from agents.accommodation.accommodation_ranker import rank_accommodations

logger = logging.getLogger(__name__)

def process_accommodation_request(request: AccommodationRequest) -> AccommodationResponse:
    """
    Main entry point for Accommodation Agent logic.
    """
    plan = []
    
    # Rough daily budget allocation for accommodation (assuming e.g. 30% of total budget goes to accommodation)
    # LKR to USD conversion approx 300
    # For a real system we would know exactly, but here we just pass a heuristic to the ranker
    daily_budget_estimate_lkr = (request.budget.amount * 300 * 0.3) / max(1, sum(s.nights for s in request.stays))
    if request.budget.currency == "LKR":
        daily_budget_estimate_lkr = (request.budget.amount * 0.3) / max(1, sum(s.nights for s in request.stays))
        
    for stay in request.stays:
        city = stay.city
        nights = stay.nights
        
        # 1. Discovery
        candidates = fetch_accommodations_geoapify(city)
        if not candidates:
            logger.info(f"Geoapify found no candidates for {city}, trying OSM.")
            candidates = fetch_accommodations_osm(city)
            
        # 2. Deduplicate
        seen_names = set()
        unique_candidates = []
        for c in candidates:
            # simple deduplication by name
            if c.name.lower() not in seen_names:
                seen_names.add(c.name.lower())
                unique_candidates.append(c)
                
        # 3. Enrich
        enriched = enrich_accommodations_google_places(unique_candidates)
        
        # 4. Pricing
        priced = [estimate_accommodation_price(c, daily_budget_estimate_lkr) for c in enriched]
        
        # 5. Ranking
        ranked = rank_accommodations(
            candidates=priced,
            travel_type=request.travel_type,
            travel_pace=request.travel_pace,
            interests=request.interests,
            daily_budget_estimate=daily_budget_estimate_lkr
        )
        
        # 6. Select top 3-4 options
        top_options = ranked[:4]
        
        selected_id = None
        if top_options:
            top_options[0].is_selected = True
            selected_id = top_options[0].accommodation_id
            
        dest_acc = DestinationAccommodation(
            city=city,
            nights=nights,
            selected_accommodation_id=selected_id,
            hotel_options=top_options
        )
        plan.append(dest_acc)
        
    return AccommodationResponse(
        status="success",
        accommodation_plan=plan
    )
