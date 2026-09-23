import httpx
import logging
from typing import Optional
from database.core.config import GEOAPIFY_API_KEY, GEOAPIFY_ROUTING_URL
from agents.planner.route.schemas import Coordinate, RoadRouteData

logger = logging.getLogger(__name__)

async def get_route(origin: Coordinate, destination: Coordinate, mode: str = "drive") -> Optional[RoadRouteData]:
    """
    Get a route between two coordinates using Geoapify.
    Supported modes typically include: drive, walk, transit, bicycle.
    """
    if not GEOAPIFY_API_KEY:
        logger.warning("GEOAPIFY_API_KEY is not set. Skipping routing.")
        return None

    # Geoapify routing uses waypoints as lat,lon|lat,lon
    waypoints = f"{origin.latitude},{origin.longitude}|{destination.latitude},{destination.destination.longitude}" if hasattr(destination, 'destination') else f"{origin.latitude},{origin.longitude}|{destination.latitude},{destination.longitude}"

    params = {
        "waypoints": waypoints,
        "mode": mode,
        "apiKey": GEOAPIFY_API_KEY
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(GEOAPIFY_ROUTING_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            features = data.get("features", [])
            
            if not features:
                logger.warning(f"No routes found between {origin} and {destination}")
                return None
                
            first_route = features[0]
            properties = first_route.get("properties", {})
            geometry = first_route.get("geometry")
            
            # Distance is typically in meters, time in seconds
            distance_km = properties.get("distance", 0) / 1000.0
            duration_min = properties.get("time", 0) / 60.0
            
            instructions_raw = properties.get("legs", [{}])[0].get("steps", [])
            instructions = [step.get("instruction", {}).get("text", "") for step in instructions_raw if "instruction" in step]
            
            return RoadRouteData(
                distance_km=round(distance_km, 2),
                estimated_duration_minutes=round(duration_min, 2),
                mode=mode,
                route_geometry=geometry,
                instructions=instructions
            )
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Geoapify API HTTP error during routing: {e.response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Network error during routing: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during routing: {e}")
        
    return None
