import logging
from typing import Dict, Any, List

from state import TripState
from services.destination.destination_recommender import recommend_from_traveller_profile

logger = logging.getLogger(__name__)

async def process_destination(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node — Agent 2 (Destination & Experience).
    Priority order:
      1. must_visit_destinations from profile (always included)
      2. preferred_destinations from profile (included if slots available)
      3. AI-recommended destinations (fill remaining slots)
    """
    logger.info("Executing Destination Node")
    
    profile = state.get("profile")
    if not profile:
        logger.warning("No profile provided, skipping destination recommendation.")
        return {}
        
    try:
        profile_dict = profile.model_dump()
        
        must_visit = list(profile.must_visit_destinations or [])
        preferred = list(profile.preferred_destinations or [])
        
        logger.info(f"Profile must_visit_destinations: {must_visit}")
        logger.info(f"Profile preferred_destinations: {preferred}")
        
        # Call existing interest-based recommender
        # Request more attractions per city so multi-day stays have enough content
        dest_result = recommend_from_traveller_profile(
            profile_dict,
            top_destinations=5,
            top_attractions=8,   # Increased from 3 to ensure rich itineraries
            debug=False
        )
        
        ai_destinations = dest_result.get("recommended_destinations", [])
        logger.info(f"AI recommended destinations: {[d.get('destination') for d in ai_destinations]}")
        
        # Build final destination list with priority ordering
        final_destinations: List[Dict[str, Any]] = []
        seen_cities = set()
        
        def normalise(name: str) -> str:
            return name.lower().strip()
        
        def _find_or_stub_destination(city_name: str, ai_list: List[Dict]) -> Dict:
            """Return an AI result for the city if available, else create a stub."""
            norm = normalise(city_name)
            for d in ai_list:
                d_name = d.get("destination") or d.get("city", "")
                if normalise(d_name) == norm:
                    # Ensure consistent key
                    d.setdefault("city", d.get("destination", city_name))
                    return d
            # Stub: keeps attractions empty — schedule will still assign a day
            return {
                "city": city_name,
                "destination": city_name,
                "score": 0.0,
                "interest_coverage": 0.0,
                "matching_attractions": 0,
                "strong_attractions": 0,
                "attractions": [],
                "source": "user_requested"
            }
        
        # 1. Must-visit (always first, ordered as user specified)
        for city in must_visit:
            norm = normalise(city)
            if norm not in seen_cities:
                final_destinations.append(_find_or_stub_destination(city, ai_destinations))
                seen_cities.add(norm)
        
        # 2. Preferred destinations
        for city in preferred:
            norm = normalise(city)
            if norm not in seen_cities:
                final_destinations.append(_find_or_stub_destination(city, ai_destinations))
                seen_cities.add(norm)
        
        # 3. AI recommendations (fill remaining slots up to max 4 total destinations)
        target = max(3, profile.duration_days // 2 if profile.duration_days else 3)
        for d in ai_destinations:
            if len(final_destinations) >= target:
                break
            city_name = d.get("destination") or d.get("city", "")
            norm = normalise(city_name)
            if norm and norm not in seen_cities:
                d.setdefault("city", city_name)
                final_destinations.append(d)
                seen_cities.add(norm)
        
        # Ensure minimum 1 destination
        if not final_destinations:
            final_destinations = ai_destinations[:3]
            
        logger.info(f"Final destinations for trip: {[d.get('city') or d.get('destination') for d in final_destinations]}")
        
        return {"destinations": final_destinations}
    except Exception as e:
        logger.error(f"Error in Destination Node: {str(e)}", exc_info=True)
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Destination recommendation failed: {str(e)}"]}
