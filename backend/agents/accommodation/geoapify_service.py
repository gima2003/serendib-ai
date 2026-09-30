import os
import httpx
import logging
import uuid
from typing import List
from agents.accommodation.schemas import AccommodationCandidate

logger = logging.getLogger(__name__)

# Basic Sri Lankan city bounding boxes or center points could be used,
# but for simplicity we will rely on Geoapify text search or passing city names.

def fetch_accommodations_geoapify(city: str) -> List[AccommodationCandidate]:
    """
    Fetches accommodation candidates from Geoapify for a given city.
    """
    api_key = os.getenv("GEOAPIFY_API_KEY")
    candidates = []
    
    if not api_key:
        logger.warning("GEOAPIFY_API_KEY is missing. Skipping Geoapify discovery.")
        return candidates
        
    url = "https://api.geoapify.com/v2/places"
    # We first need to get the bounding box or coordinates of the city to do a radius/bbox search, 
    # but Geoapify text search might be simpler if we don't have lat/lon.
    # We will use geocoding to get the city coordinates first, or assume we have them.
    # To keep it robust without multiple API calls, we'll try a generic filter or search.
    # For a real system, we'd geocode the city first. Let's do a quick geocode.
    
    geocode_url = "https://api.geoapify.com/v1/geocode/search"
    try:
        geo_resp = httpx.get(geocode_url, params={"text": f"{city}, Sri Lanka", "apiKey": api_key}, timeout=10.0)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        
        if not geo_data.get("features"):
            logger.warning(f"Could not geocode city {city} using Geoapify.")
            return candidates
            
        # Get the first result's coordinates
        lon, lat = geo_data["features"][0]["geometry"]["coordinates"]
        
        # Now search for accommodation near this point
        params = {
            "categories": "accommodation.hotel,accommodation.guest_house,accommodation.hostel,accommodation.chalet",
            "filter": f"circle:{lon},{lat},10000", # 10km radius
            "limit": 20,
            "apiKey": api_key
        }
        
        resp = httpx.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            name = props.get("name")
            if not name:
                continue
                
            acc_type = props.get("categories", ["accommodation"])[0].split(".")[-1]
            
            candidate = AccommodationCandidate(
                accommodation_id=f"GEO_{uuid.uuid4().hex[:8]}",
                name=name,
                city=city,
                address=props.get("formatted"),
                latitude=props.get("lat"),
                longitude=props.get("lon"),
                accommodation_type=acc_type.replace("_", " ").title(),
                source="Geoapify",
                source_confidence="high",
                # Geoapify doesn't reliably provide prices or ratings in the free tier basic response
            )
            candidates.append(candidate)
            
    except Exception as e:
        logger.error(f"Error fetching accommodations from Geoapify for {city}: {e}")
        
    return candidates
