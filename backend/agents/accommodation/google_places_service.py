import os
import httpx
import logging
from typing import List
from agents.accommodation.schemas import AccommodationCandidate

logger = logging.getLogger(__name__)

def enrich_accommodations_google_places(candidates: List[AccommodationCandidate]) -> List[AccommodationCandidate]:
    """
    Enriches accommodation candidates using Google Places API if available.
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        logger.info("GOOGLE_PLACES_API_KEY not found. Skipping Google Places enrichment.")
        return candidates
        
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.rating,places.userRatingCount,places.priceLevel",
        "Content-Type": "application/json"
    }
    
    for candidate in candidates:
        try:
            payload = {
                "textQuery": f"{candidate.name} {candidate.city} Sri Lanka"
            }
            resp = httpx.post(url, headers=headers, json=payload, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                places = data.get("places", [])
                if places:
                    place = places[0]
                    if "rating" in place:
                        candidate.rating = place["rating"]
                    if "userRatingCount" in place:
                        candidate.review_count = place["userRatingCount"]
                    # We could also use priceLevel to help estimate price later
                    # priceLevel ranges from 0 to 4
        except Exception as e:
            logger.error(f"Error enriching {candidate.name} with Google Places: {e}")
            
    return candidates
