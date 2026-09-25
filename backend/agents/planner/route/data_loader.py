import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "planner"

def load_csv_data(filepath: Path, engine: str = 'c') -> pd.DataFrame:
    """Helper function to load a CSV file with error handling."""
    if not filepath.exists():
        logger.error(f"Dataset not found at: {filepath}")
        raise FileNotFoundError(f"Missing dataset: {filepath}")
        
    read_kwargs = {'encoding': 'utf-8', 'on_bad_lines': 'skip', 'engine': engine}
    if engine == 'c':
        read_kwargs['low_memory'] = False
        
    try:
        try:
            df = pd.read_csv(filepath, **read_kwargs)
        except UnicodeDecodeError:
            logger.warning(f"UTF-8 decoding failed for {filepath.name}, falling back to latin1.")
            read_kwargs['encoding'] = 'latin1'
            df = pd.read_csv(filepath, **read_kwargs)
            
        if df.empty:
            logger.warning(f"Dataset is empty: {filepath}")
            
        return df
    except Exception as e:
        logger.error(f"Unreadable CSV dataset at {filepath}: {e}")
        raise ValueError(f"Unreadable CSV dataset at {filepath}: {e}") from e

def load_roads(filepath: Path = None) -> pd.DataFrame:
    """Loads the roads dataset."""
    if filepath is None:
        filepath = BASE_DIR / "roads" / "sri_lanka_all_roads.csv"
    return load_csv_data(filepath, engine='python')

def load_bus_fares(filepath: Path = None) -> pd.DataFrame:
    """Loads the bus fares dataset."""
    if filepath is None:
        filepath = BASE_DIR / "roads" / "bus_fares_clean.csv"
    return load_csv_data(filepath)

def load_scenic_places(filepath: Path = None) -> pd.DataFrame:
    """Loads the scenic places dataset."""
    if filepath is None:
        filepath = BASE_DIR / "roads" / "sri_lanka_osm_scenic_places.csv"
    return load_csv_data(filepath)
