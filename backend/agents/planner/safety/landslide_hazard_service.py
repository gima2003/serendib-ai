import os
import geopandas as gpd
from shapely.geometry import Point
from typing import Dict, Any

_hazard_gdf = None

def load_hazard_map():
    global _hazard_gdf
    if _hazard_gdf is None:
        data_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "data", "planner", "safety", "processed", "landslide_hazard.geojson"
        ))
        if os.path.exists(data_path):
            _hazard_gdf = gpd.read_file(data_path)
        else:
            _hazard_gdf = gpd.GeoDataFrame(columns=['Range', 'geometry'], geometry='geometry', crs="EPSG:4326")
    return _hazard_gdf

def check_hazard_level(latitude: float, longitude: float) -> Dict[str, Any]:
    gdf = load_hazard_map()
    point = Point(longitude, latitude)
    
    # Filter bounds to speed up check if the index isn't available
    # sindex can be used for spatial queries to speed this up significantly
    if not gdf.empty and gdf.sindex is not None:
        possible_matches_index = list(gdf.sindex.intersection(point.bounds))
        possible_matches = gdf.iloc[possible_matches_index]
        intersecting = possible_matches[possible_matches.intersects(point)]
    else:
        intersecting = gdf[gdf.intersects(point)]
        
    if not intersecting.empty:
        max_range = int(intersecting['Range'].max())
    else:
        max_range = 1  # Default to LOW
        
    risk_mapping = {
        1: "LOW",
        2: "MODERATE",
        3: "HIGH",
        4: "VERY_HIGH"
    }
    
    return {
        "hazard_range": max_range,
        "risk_level": risk_mapping.get(max_range, "LOW"),
        "source": "LHMP_50000"
    }
