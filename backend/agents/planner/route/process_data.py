import logging
from pathlib import Path
from data_loader import load_roads, load_bus_fares, load_scenic_places, BASE_DIR
from data_cleaner import clean_roads_data, clean_bus_fares_data, clean_scenic_places_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting data foundation processing for Route Agent.")
    
    roads_dir = BASE_DIR / "roads"
    
    try:
        # Roads
        logger.info("Processing roads data...")
        raw_roads = load_roads()
        clean_roads = clean_roads_data(raw_roads)
        roads_out_path = roads_dir / "sri_lanka_all_roads_clean.csv"
        clean_roads.to_csv(roads_out_path, index=False)
        logger.info(f"Saved cleaned roads dataset to {roads_out_path}")
        
        # Bus Fares
        logger.info("Processing bus fares data...")
        raw_bus = load_bus_fares()
        clean_bus = clean_bus_fares_data(raw_bus)
        bus_out_path = roads_dir / "bus_fares_clean_validated.csv"
        clean_bus.to_csv(bus_out_path, index=False)
        logger.info(f"Saved cleaned bus fares dataset to {bus_out_path}")
        
        # Scenic Places
        logger.info("Processing scenic places data...")
        raw_scenic = load_scenic_places()
        clean_scenic = clean_scenic_places_data(raw_scenic)
        scenic_out_path = roads_dir / "sri_lanka_osm_scenic_places_clean.csv"
        clean_scenic.to_csv(scenic_out_path, index=False)
        logger.info(f"Saved cleaned scenic places dataset to {scenic_out_path}")
        
        logger.info("Data foundation processing completed successfully.")
        
    except Exception as e:
        logger.error(f"Data processing failed: {e}")

if __name__ == "__main__":
    main()
