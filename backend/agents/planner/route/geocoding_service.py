import httpx
import logging
from typing import Optional
from database.core.config import GEOAPIFY_API_KEY, GEOAPIFY_GEOCODING_URL
from agents.planner.route.schemas import Coordinate

logger = logging.getLogger(__name__)

# Lightweight in-memory cache for development
_GEOCODE_CACHE = {}

async def geocode_location(location_name: str, skip_cache: bool = False) -> Optional[Coordinate]:
    """
    Geocode a location string into a Coordinate using Geoapify.
    Adds 'Sri Lanka' context to reduce ambiguity.
    """
    normalized_name = location_name.strip().lower()
    
    if not skip_cache and normalized_name in _GEOCODE_CACHE:
        return _GEOCODE_CACHE[normalized_name]

    if not GEOAPIFY_API_KEY:
        logger.warning("GEOAPIFY_API_KEY is not set. Skipping geocoding.")
        return None

    query = f"{location_name}, Sri Lanka"
    
    params = {
        "text": query,
        "apiKey": GEOAPIFY_API_KEY,
        "format": "json",
        "limit": 1
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(GEOAPIFY_GEOCODING_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                logger.warning(f"No geocoding results found for {query}")
                return None
                
            first_result = results[0]
            coord = Coordinate(
                latitude=first_result.get("lat"),
                longitude=first_result.get("lon")
            )
            
            _GEOCODE_CACHE[normalized_name] = coord
            return coord
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Geoapify API HTTP error during geocoding: {e.response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Network error during geocoding: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during geocoding for {location_name}: {e}")
        
    return None
