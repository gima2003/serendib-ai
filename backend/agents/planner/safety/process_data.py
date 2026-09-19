import os
import pandas as pd
import geopandas as gpd
from data_loader import (
    load_landslide_incidents,
    load_landslide_hazard_map,
    load_landslide_footprints,
    DATA_DIR
)
from data_cleaner import (
    clean_landslide_incidents,
    clean_landslide_hazard_map,
    clean_landslide_footprints
)

def main():
    print("Starting data processing pipeline...\n")
    
    processed_dir = os.path.join(DATA_DIR, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # 1. Process Landslide Incidents
    # -------------------------------------------------------------------------
    print("--- Processing Landslide Incidents ---")
    df_incidents = load_landslide_incidents()
    orig_incidents_count = len(df_incidents)
    
    duplicates_incidents = df_incidents.duplicated().sum()
    missing_incidents = df_incidents.isna().sum().sum()
    
    # Check invalid coordinates
    if 'Latitude' in df_incidents.columns and 'Longitude' in df_incidents.columns:
        lat = pd.to_numeric(df_incidents['Latitude'], errors='coerce')
        lon = pd.to_numeric(df_incidents['Longitude'], errors='coerce')
        valid_mask = (lat.notna() & lon.notna() & (lat >= -90) & (lat <= 90) & (lon >= -180) & (lon <= 180))
        invalid_coords_incidents = (~valid_mask).sum()
    else:
        invalid_coords_incidents = 0
        
    df_incidents_clean = clean_landslide_incidents(df_incidents)
    clean_incidents_count = len(df_incidents_clean)
    
    print(f"Original row count: {orig_incidents_count}")
    print(f"Cleaned row count: {clean_incidents_count}")
    print(f"Duplicate count: {duplicates_incidents}")
    print(f"Missing values: {missing_incidents}")
    print(f"Invalid coordinates: {invalid_coords_incidents}\n")
    
    out_incidents = os.path.join(processed_dir, "landslide_incidents_clean.csv")
    df_incidents_clean.to_csv(out_incidents, index=False)
    
    # -------------------------------------------------------------------------
    # 2. Process Landslide Hazard Map
    # -------------------------------------------------------------------------
    print("--- Processing LHMP Shapefile ---")
    gdf_lhmp = load_landslide_hazard_map()
    orig_lhmp_count = len(gdf_lhmp)
    
    # GeoDataFrame might have duplicates too, but we don't clean them based on instructions. We'll still print it if possible, else 0
    try:
        # dropping geometry to check for attribute duplicates
        duplicates_lhmp = pd.DataFrame(gdf_lhmp.drop(columns='geometry')).duplicated().sum()
    except:
        duplicates_lhmp = 0
        
    missing_lhmp = gdf_lhmp.isna().sum().sum()
    
    # Invalid coordinates (geometry)
    invalid_coords_lhmp = (~gdf_lhmp.geometry.is_valid | gdf_lhmp.geometry.is_empty | gdf_lhmp.geometry.isna()).sum()
    
    gdf_lhmp_clean = clean_landslide_hazard_map(gdf_lhmp)
    clean_lhmp_count = len(gdf_lhmp_clean)
    
    print(f"Original row count: {orig_lhmp_count}")
    print(f"Cleaned row count: {clean_lhmp_count}")
    print(f"Duplicate count: {duplicates_lhmp}")
    print(f"Missing values: {missing_lhmp}")
    print(f"Invalid coordinates (geometry): {invalid_coords_lhmp}\n")
    
    print("LHMP Hazard Distribution:")
    if 'Range' in gdf_lhmp_clean.columns:
        dist = gdf_lhmp_clean['Range'].value_counts().sort_index()
        for r_val, count in dist.items():
            print(f"Range {int(r_val)}:")
            print(f"{count} records")
    print("")
    
    out_lhmp = os.path.join(processed_dir, "landslide_hazard.geojson")
    if os.path.exists(out_lhmp):
        os.remove(out_lhmp)
    gdf_lhmp_clean.to_file(out_lhmp, driver="GeoJSON")
    
    # -------------------------------------------------------------------------
    # 3. Process Landslide Footprints
    # -------------------------------------------------------------------------
    print("--- Processing Landslide Footprints ---")
    df_footprints = load_landslide_footprints()
    orig_footprints_count = len(df_footprints)
    
    duplicates_footprints = df_footprints.duplicated().sum()
    missing_footprints = df_footprints.isna().sum().sum()
    
    # Invalid coordinates (no geometry)
    invalid_coords_footprints = 0
    if 'geometry_wkt' in df_footprints.columns:
        wkt_nulls = df_footprints['geometry_wkt'].replace('nan', pd.NA).replace('', pd.NA).isna().sum()
        invalid_coords_footprints = wkt_nulls
    
    df_footprints_clean = clean_landslide_footprints(df_footprints)
    clean_footprints_count = len(df_footprints_clean)
    
    print(f"Original row count: {orig_footprints_count}")
    print(f"Cleaned row count: {clean_footprints_count}")
    print(f"Duplicate count: {duplicates_footprints}")
    print(f"Missing values: {missing_footprints}")
    print(f"Invalid coordinates (missing geometry): {invalid_coords_footprints}\n")
    
    out_footprints = os.path.join(processed_dir, "landslide_footprints_clean.csv")
    df_footprints_clean.to_csv(out_footprints, index=False)
    
    print("Processed files created successfully in data/planner/safety/processed/")

if __name__ == "__main__":
    main()
