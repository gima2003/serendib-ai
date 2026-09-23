import sys
import logging
import pandas as pd
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

# Add planner dir to sys.path to import route module
planner_dir = Path(__file__).resolve().parent.parent
if str(planner_dir) not in sys.path:
    sys.path.append(str(planner_dir))

from route.data_cleaner import clean_text_series

def clean_train_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the train prices dataset.
    """
    logger.info(f"Cleaning train prices data. Initial rows: {len(df)}")
    
    # Trim whitespace and normalize columns
    df.columns = df.columns.str.strip()
    
    # Remove exact duplicates
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        logger.info(f"Removing {duplicates_count} duplicate rows in train prices.")
    df = df.drop_duplicates()
    
    # 1. Trim whitespace from Station
    if 'Station' in df.columns:
        df['Station'] = clean_text_series(df['Station'])
        df['station_valid'] = df['Station'].notna() & (df['Station'] != "")
    
    # 2. Convert Distance_Km to numeric safely
    if 'Distance_Km' in df.columns:
        df['Distance_Km'] = pd.to_numeric(df['Distance_Km'], errors='coerce')
        # Negative distances are invalid
        invalid_dist_mask = df['Distance_Km'] < 0
        if invalid_dist_mask.sum() > 0:
            logger.warning(f"Detected {invalid_dist_mask.sum()} negative distance values.")
        df['distance_valid'] = df['Distance_Km'].notna() & (~invalid_dist_mask)
    
    # 3. Convert fare columns safely, preserve 0s
    fare_cols = ['1st_Class_Rs', '2nd_Class_Rs', '3rd_Class_Rs']
    is_fare_valid = pd.Series(True, index=df.index)
    for col in fare_cols:
        if col in df.columns:
            # Coerce to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
            negative_mask = df[col] < 0
            if negative_mask.sum() > 0:
                logger.warning(f"Detected {negative_mask.sum()} negative fare values in {col}.")
            # A valid fare row has numeric, non-negative values
            is_fare_valid = is_fare_valid & df[col].notna() & (~negative_mask)
            
    df['fare_valid'] = is_fare_valid
    
    # Detect missing or invalid station names
    if 'station_valid' in df.columns:
        missing_stations = (~df['station_valid']).sum()
        if missing_stations > 0:
            logger.warning(f"Detected {missing_stations} missing or invalid station names.")
        
    logger.info(f"Finished cleaning train prices data. Final rows: {len(df)}")
    return df

def clean_taxi_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the taxi rates dataset.
    """
    logger.info(f"Cleaning taxi rates data. Initial rows: {len(df)}")
    
    # Trim whitespace and normalize columns
    df.columns = df.columns.str.strip()
    
    # Remove exact duplicates
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        logger.info(f"Removing {duplicates_count} duplicate rows in taxi rates.")
    df = df.drop_duplicates()
    
    # 1. Trim whitespace for text columns
    text_cols = ['mode', 'provider', 'availability', 'vehicle_type']
    for col in text_cols:
        if col in df.columns:
            df[col] = clean_text_series(df[col])
            
    if 'availability' in df.columns:
        df['availability'] = df['availability'].str.lower()
        
    def process_price_col(col_name):
        if col_name in df.columns:
            # Check for "on_request" text
            raw_text = clean_text_series(df[col_name])
            is_on_request = raw_text.str.lower() == 'on_request'
            num_on_request = is_on_request.sum()
            if num_on_request > 0:
                logger.info(f"Found {num_on_request} 'on_request' values in {col_name}.")
            
            # To preserve source info ("on_request"), we create a clean string column as raw
            df[f'{col_name}_raw'] = raw_text
            
            # Convert the main column to numeric, replacing 'on_request' with NaN
            numeric_series = pd.to_numeric(df[col_name], errors='coerce')
            
            # Check for negative prices
            negatives = numeric_series < 0
            if negatives.sum() > 0:
                logger.warning(f"Detected {negatives.sum()} negative prices in {col_name}.")
                
            available_flag = numeric_series.notna() & (~negatives)
            
            df[col_name] = numeric_series
            df[f'{col_name}_available'] = available_flag
            
            return available_flag, num_on_request
        return pd.Series(True, index=df.index), 0

    base_fare_avail, on_request_base = process_price_col('base_fare')
    per_km_avail, on_request_km = process_price_col('per_km')
    
    total_on_request = on_request_base + on_request_km
    logger.info(f"Total 'on_request' prices discovered in base_fare and per_km: {total_on_request}")
    
    # Valid pricing if at least some pricing component is available OR it's explicitly on_request
    df['pricing_valid'] = base_fare_avail | per_km_avail | (df['availability'] == 'on_request')
    
    logger.info(f"Finished cleaning taxi rates data. Final rows: {len(df)}")
    return df
