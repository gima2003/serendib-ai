import os
import pandas as pd
import geopandas as gpd

DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "data", "planner", "safety"
    )
)

def load_landslide_incidents():
    file_path = os.path.join(DATA_DIR, "incidents", "All_Sri_Lanka_Master.csv")
    return pd.read_csv(file_path, low_memory=False)

def load_landslide_hazard_map():
    # Set env var to prevent shapely crashes on invalid geometries (unclosed rings)
    os.environ['OGR_GEOMETRY_ACCEPT_UNCLOSED_RING'] = 'NO'
    file_path = os.path.join(DATA_DIR, "LHMP_50000", "LHMP_50000.shp")
    return gpd.read_file(file_path)

def load_landslide_footprints():
    file_path = os.path.join(DATA_DIR, "footprints", "All_Sri_Lanka_Polygons.csv")
    return pd.read_csv(file_path, low_memory=False)
