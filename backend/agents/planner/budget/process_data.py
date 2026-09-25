import logging
from pathlib import Path
import sys

# Note: imports within budget use planner level imports

from data_loader import load_train_prices, load_taxi_rates, TRANSPORT_DIR
from data_cleaner import clean_train_prices, clean_taxi_rates

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting data foundation processing for Budget Agent.")
    
    try:
        # Train Prices
        logger.info("Processing train prices data...")
        raw_train = load_train_prices()
        clean_train = clean_train_prices(raw_train)
        
        logger.info(f"Train missing values after cleaning: \n{clean_train.isna().sum()}")
        
        train_out_path = TRANSPORT_DIR / "train_price_clean.csv"
        clean_train.to_csv(train_out_path, index=False)
        logger.info(f"Saved cleaned train prices dataset to {train_out_path}")
        
        # Taxi Rates
        logger.info("Processing taxi rates data...")
        raw_taxi = load_taxi_rates()
        clean_taxi = clean_taxi_rates(raw_taxi)
        
        logger.info(f"Taxi missing values after cleaning: \n{clean_taxi.isna().sum()}")
        
        taxi_out_path = TRANSPORT_DIR / "taxi_rates_clean.csv"
        clean_taxi.to_csv(taxi_out_path, index=False)
        logger.info(f"Saved cleaned taxi rates dataset to {taxi_out_path}")
        
        logger.info("Data foundation processing for Budget completed successfully.")
        
    except Exception as e:
        logger.error(f"Data processing failed: {e}")

if __name__ == "__main__":
    main()
