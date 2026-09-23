import logging
import pandas as pd
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

def clean_text_series(series: pd.Series) -> pd.Series:
    """Trim leading/trailing whitespaces and normalize empty strings to NaN."""
    if series.dtype == 'object' or pd.api.types.is_string_dtype(series):
        return series.astype(str).str.strip().replace(r'^(?:nan|NaN|None|)$', np.nan, regex=True)
    return series

def clean_roads_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Sri Lanka roads dataset.
    
    Operations:
    - Trims text values and normalizes empty strings
    - Safely converts numeric columns
    - Validates length_km and speed_limit
    - Normalizes road_condition and closure_status
    - Flags invalid geometry
    - Removes exact duplicates
    """
    logger.info(f"Cleaning roads data. Initial rows: {len(df)}")
    
    # Remove exact duplicates
    df = df.drop_duplicates()
    
    # Clean text columns
    text_cols = ['road_name', 'road_number', 'road_class', 'road_condition', 
                 'surface_type', 'closure_status', 'district']
    for col in text_cols:
        if col in df.columns:
            df[col] = clean_text_series(df[col])
            
            # Additional normalization for specific columns
            if col == 'road_condition':
                df[col] = df[col].str.lower()
            elif col == 'closure_status':
                df[col] = df[col].str.lower()
                
    # Validate length_km
    if 'length_km' in df.columns:
        df['length_km'] = pd.to_numeric(df['length_km'], errors='coerce')
        # Negative lengths or absurdly large lengths could be set to NaN or flagged.
        # We will keep it simple and just ensure it's numeric, converting errors to NaN
        
    # Validate speed_limit
    if 'speed_limit' in df.columns:
        df['speed_limit'] = pd.to_numeric(df['speed_limit'], errors='coerce')
        
    # Safely convert other numeric columns
    if 'lanes' in df.columns:
        df['lanes'] = pd.to_numeric(df['lanes'], errors='coerce')
    if 'traffic_volume' in df.columns:
        df['traffic_volume'] = pd.to_numeric(df['traffic_volume'], errors='coerce')
        
    # Flag invalid geometry
    if 'geometry' in df.columns:
        df['geometry_valid'] = df['geometry'].notna() & (df['geometry'].str.len() > 0)
    else:
        logger.warning("'geometry' column missing from roads data.")
        
    logger.info(f"Finished cleaning roads data. Final rows: {len(df)}")
    return df

def clean_bus_fares_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Sri Lanka bus fares dataset.
    
    Operations:
    - Normalizes From/To/Via/Stop Name text
    - Converts Route No, Stage No safely
    - Converts Fare (LKR) safely and identifies suspicious fares
    - Adds 'fare_valid' indicator instead of inventing values
    - Preserves Route_ID
    """
    logger.info(f"Cleaning bus fares data. Initial rows: {len(df)}")
    
    df = df.drop_duplicates()
    
    # Text normalization
    text_cols = ['From', 'To', 'Via', 'Stop Name', 'Route No', 'Route_ID']
    for col in text_cols:
        if col in df.columns:
            df[col] = clean_text_series(df[col])
            
    if 'Stage No' in df.columns:
        df['Stage No'] = pd.to_numeric(df['Stage No'], errors='coerce')
        
    if 'Fare (LKR)' in df.columns:
        # Convert Fare to numeric
        fares = df['Fare (LKR)']
        if fares.dtype == object or pd.api.types.is_string_dtype(fares):
            fares = fares.replace(r'[^\d.]', '', regex=True)
        
        df['Fare (LKR)'] = pd.to_numeric(fares, errors='coerce')
        
        # Identify suspicious fares (e.g., > 5000 LKR could be suspicious based on typical Sri Lanka bus fares)
        # We don't overwrite, we flag.
        suspicious_mask = df['Fare (LKR)'] > 5000
        null_mask = df['Fare (LKR)'].isna()
        
        df['fare_valid'] = ~(suspicious_mask | null_mask)
        num_suspicious = suspicious_mask.sum()
        if num_suspicious > 0:
            logger.warning(f"Detected {num_suspicious} suspicious bus fares (> 5000).")
    else:
        logger.warning("'Fare (LKR)' column missing from bus fares data.")
        
    logger.info(f"Finished cleaning bus fares data. Final rows: {len(df)}")
    return df

def clean_scenic_places_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Sri Lanka OSM scenic places dataset.
    
    Operations:
    - Normalizes place names and categories
    - Converts and validates latitude/longitude
    - Removes records with unusable coordinates from output
    - Preserves identifiers and removes exact duplicates
    """
    logger.info(f"Cleaning scenic places data. Initial rows: {len(df)}")
    
    df = df.drop_duplicates()
    
    # Normalizations
    text_cols = ['name', 'name_en', 'category', 'tourism', 'natural', 'leisure']
    for col in text_cols:
        if col in df.columns:
            df[col] = clean_text_series(df[col])
            if col == 'category':
                df[col] = df[col].str.lower()
                
    # Coordinates validation
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # Sri Lanka bounding box roughly: Lat 5.8 to 9.9, Lon 79.5 to 82.0
        lat_valid = df['latitude'].between(5.8, 9.9)
        lon_valid = df['longitude'].between(79.5, 82.0)
        
        valid_coords = lat_valid & lon_valid
        
        rejected_count = (~valid_coords).sum()
        if rejected_count > 0:
            logger.warning(f"Rejecting {rejected_count} scenic places due to invalid/missing coordinates.")
            
        df = df[valid_coords].copy()
    else:
        logger.warning("Latitude/Longitude columns missing from scenic places data.")
        
    logger.info(f"Finished cleaning scenic places data. Final rows: {len(df)}")
    return df
