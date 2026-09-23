import logging
import math
from typing import List
from agents.planner.route.data_loader import load_scenic_places
from agents.planner.route.schemas import Coordinate, ScenicPlace

logger = logging.getLogger(__name__)

SCENIC_ROUTE_RADIUS_KM = 20.0

try:
    _SCENIC_DF = load_scenic_places()
except Exception as e:
    logger.error(f"Failed to load scenic places dataset: {e}")
    _SCENIC_DF = None

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points in km."""
    R = 6371.0 # Earth radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_scenic_places_near_route(origin: Coordinate, destination: Coordinate, radius_km: float = SCENIC_ROUTE_RADIUS_KM) -> List[ScenicPlace]:
    """
    Find scenic places reasonably close to the route.
    For V1, without full linestring interpolation, we check proximity to the origin-destination bounding box/midpoints.
    """
    if _SCENIC_DF is None or _SCENIC_DF.empty:
        return []

    places = []
    try:
        # Interpolate a few points along the straight line as a heuristic for the route
        num_points = 5
        lats = [origin.latitude + i * (destination.latitude - origin.latitude) / num_points for i in range(num_points + 1)]
        lons = [origin.longitude + i * (destination.longitude - origin.longitude) / num_points for i in range(num_points + 1)]
        route_points = list(zip(lats, lons))

        for _, row in _SCENIC_DF.iterrows():
            p_lat = row.get('latitude')
            p_lon = row.get('longitude')
            
            if not p_lat or not p_lon or math.isnan(p_lat) or math.isnan(p_lon):
                continue
                
            # Find minimum distance to any route point
            min_dist = min([haversine(rp[0], rp[1], p_lat, p_lon) for rp in route_points])
            
            if min_dist <= radius_km:
                name = str(row.get('name', 'Unknown'))
                if name == 'nan':
                    name = str(row.get('name_en', 'Unknown'))
                    
                places.append(ScenicPlace(
                    name=name,
                    category=str(row.get('category', 'unknown')),
                    latitude=p_lat,
                    longitude=p_lon,
                    distance_from_route_km=round(min_dist, 2),
                    source=str(row.get('source', 'OSM'))
                ))
                
        # Sort by distance
        places.sort(key=lambda x: x.distance_from_route_km)
        
        # Limit to top 5 to avoid overwhelming the response
        return places[:5]
        
    except Exception as e:
        logger.warning(f"Error extracting scenic places: {e}")

    return []
