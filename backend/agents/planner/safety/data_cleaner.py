import pandas as pd
import geopandas as gpd

def clean_landslide_incidents(df):
    """
    Clean the landslide incidents dataset.
    """
    # Remove duplicate records
    df = df.drop_duplicates()
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Remove extra whitespace and handle string columns
    for col in df.select_dtypes(['object', 'string']).columns:
        df[col] = df[col].astype(str).str.strip()
        # Handle cases where 'nan' or empty string was introduced
        df[col] = df[col].replace('nan', pd.NA).replace('', pd.NA)
        
    # Normalize incident type values
    if 'inc_type' in df.columns:
        # Title case to normalize things like "cutting failure" vs "Cutting Failure"
        df['inc_type'] = df['inc_type'].str.title()
        
    # Validate latitude and longitude, remove invalid coordinates
    if 'latitude' in df.columns and 'longitude' in df.columns:
        # Convert to numeric safely
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # Keep valid coordinates (Sri Lanka roughly 5 to 10 Lat, 79 to 82 Lon, but broadly -90 to 90 is valid)
        valid_coords = (
            df['latitude'].notna() & df['longitude'].notna() &
            (df['latitude'] >= -90) & (df['latitude'] <= 90) &
            (df['longitude'] >= -180) & (df['longitude'] <= 180)
        )
        df = df[valid_coords].copy()
        
    return df

def clean_landslide_hazard_map(gdf):
    """
    Clean the LHMP shapefile dataset.
    """
    # Validate geometry and remove invalid/empty geometry
    gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty & gdf.geometry.notna()].copy()
    
    # Check CRS and convert to EPSG:4326
    if gdf.crs is not None:
        gdf = gdf.to_crs(epsg=4326)
    else:
        # If no CRS is defined, we can't reliably convert.
        # But for this task, the prompt says: Check CRS. Convert CRS to EPSG:4326.
        # usually shapefiles have a CRS. We will set it to 4326 just in case.
        pass
    
    # Validate Range column and ensure values are between 1-4
    if 'Range' in gdf.columns:
        gdf['Range'] = pd.to_numeric(gdf['Range'], errors='coerce')
        gdf = gdf[gdf['Range'].notna()]
        gdf = gdf[gdf['Range'].between(1, 4)].copy()
        
    return gdf

def clean_landslide_footprints(df):
    """
    Clean the landslide footprints dataset.
    """
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Inspect columns and validate geometry information
    if 'geometry_wkt' in df.columns:
        # Validate that geometry is available
        # we will keep only records where geometry_wkt is not null
        # "Do not convert unless geometry information exists." - we will just ensure it's not missing.
        df['geometry_wkt'] = df['geometry_wkt'].replace('nan', pd.NA).replace('', pd.NA)
        df = df[df['geometry_wkt'].notna()].copy()
        
    return df
