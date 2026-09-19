import os
import pandas as pd
import numpy as np
from typing import Dict, Any

_incidents_df = None

def load_incidents():
    global _incidents_df
    if _incidents_df is None:
        data_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "data", "planner", "safety", "processed", "landslide_incidents_clean.csv"
        ))
        if os.path.exists(data_path):
            _incidents_df = pd.read_csv(data_path)
            _incidents_df = _incidents_df.dropna(subset=['latitude', 'longitude']).copy()
        else:
            _incidents_df = pd.DataFrame(columns=['latitude', 'longitude', 'inc_type'])
    return _incidents_df

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def check_nearby_incidents(latitude: float, longitude: float) -> Dict[str, Any]:
    df = load_incidents()
    if df.empty or 'latitude' not in df.columns or 'longitude' not in df.columns:
        return {"nearby_incidents": 0, "incident_types": []}
        
    distances = haversine_distance(latitude, longitude, df['latitude'].values, df['longitude'].values)
    
    # 5 km radius
    nearby_mask = distances <= 5.0
    nearby = df[nearby_mask]
    
    incident_types = []
    if 'inc_type' in nearby.columns:
        incident_types = nearby['inc_type'].dropna().unique().tolist()
        
    return {
        "nearby_incidents": len(nearby),
        "incident_types": incident_types
    }
