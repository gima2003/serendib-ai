import httpx
import logging
import uuid
from typing import List
from agents.accommodation.schemas import AccommodationCandidate

logger = logging.getLogger(__name__)

def fetch_accommodations_osm(city: str) -> List[AccommodationCandidate]:
    """
    Fetches accommodation candidates from OpenStreetMap via Overpass API as a fallback.
    """
    candidates = []
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Overpass query to find hotels/guesthouses in the given city area
    query = f"""
    [out:json][timeout:25];
    area[name="{city}"]->.searchArea;
    (
      node["tourism"~"hotel|guest_house|hostel"](area.searchArea);
      way["tourism"~"hotel|guest_house|hostel"](area.searchArea);
    );
    out center 20;
    """
    
    try:
        headers = {"User-Agent": "SerendibAI/1.0", "Accept": "application/json"}
        resp = httpx.post(
            overpass_url, 
            data={"data": query},
            headers=headers,
            timeout=15.0
        )
        resp.raise_for_status()
        data = resp.json()
        
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name")
            if not name:
                continue
                
            tourism_type = tags.get("tourism", "accommodation")
            lat = element.get("lat") or element.get("center", {}).get("lat")
            lon = element.get("lon") or element.get("center", {}).get("lon")
            
            candidate = AccommodationCandidate(
                accommodation_id=f"OSM_{uuid.uuid4().hex[:8]}",
                name=name,
                city=city,
                latitude=lat,
                longitude=lon,
                accommodation_type=tourism_type.replace("_", " ").title(),
                source="OpenStreetMap",
                source_confidence="low"
            )
            candidates.append(candidate)
            
    except Exception as e:
        logger.error(f"Error fetching accommodations from OSM for {city}: {e}")
        
    return candidates
