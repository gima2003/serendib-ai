import sys
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

# Add planner dir to sys.path to import route module
planner_dir = Path(__file__).resolve().parent.parent
if str(planner_dir) not in sys.path:
    sys.path.append(str(planner_dir))

# Import shared utilities from route
from route.data_loader import load_csv_data, BASE_DIR

TRANSPORT_DIR = BASE_DIR / "transport"

def load_train_prices(filepath: Path = None) -> pd.DataFrame:
    """Loads the train prices dataset."""
    if filepath is None:
        filepath = TRANSPORT_DIR / "train_price_clean.csv"
    return load_csv_data(filepath)

def load_taxi_rates(filepath: Path = None) -> pd.DataFrame:
    """Loads the taxi rates dataset."""
    if filepath is None:
        filepath = TRANSPORT_DIR / "taxi_rates_clean.csv"
    return load_csv_data(filepath)
