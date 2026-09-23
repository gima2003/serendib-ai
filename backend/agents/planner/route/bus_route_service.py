import logging
import pandas as pd
from typing import List
from agents.planner.route.data_loader import load_bus_fares
from agents.planner.route.schemas import BusOption

logger = logging.getLogger(__name__)

try:
    _BUS_DF = load_bus_fares()
except Exception as e:
    logger.error(f"Failed to load bus fares dataset: {e}")
    _BUS_DF = None

def get_bus_options(origin_name: str, destination_name: str) -> List[BusOption]:
    """
    Search the bus dataset for routes matching origin and destination.
    """
    if _BUS_DF is None or _BUS_DF.empty:
        return []

    origin_norm = origin_name.lower().strip()
    dest_norm = destination_name.lower().strip()

    options = []
    try:
        # We look for direct matches in 'From' and 'To' or 'Stop Name'
        # Since it's a stage-based dataset, a route might have from=origin and to=destination,
        # or they might just be stops.
        # For V1, we do a basic text match on From and To.
        
        # Filter for rows where From and To match our search
        # Note: In real scenarios, we'd need to trace stages.
        if 'From' in _BUS_DF.columns and 'To' in _BUS_DF.columns:
            matches = _BUS_DF[
                (_BUS_DF['From'].str.lower().str.contains(origin_norm, na=False)) & 
                (_BUS_DF['To'].str.lower().str.contains(dest_norm, na=False))
            ]
            
            # Group by Route_ID to avoid duplicate stage reports
            for route_id, group in matches.groupby('Route_ID'):
                first_row = group.iloc[0]
                
                # Check validation status
                fare_valid = bool(first_row.get('fare_valid', False))
                fare = float(first_row.get('Fare (LKR)', 0)) if pd.notna(first_row.get('Fare (LKR)')) else None
                
                option = BusOption(
                    route_number=str(first_row.get('Route No', 'Unknown')),
                    route_id=str(route_id),
                    from_location=str(first_row.get('From', '')),
                    to_location=str(first_row.get('To', '')),
                    via=str(first_row.get('Via', '')) if pd.notna(first_row.get('Via')) else None,
                    fare_lkr=fare,
                    fare_valid=fare_valid
                )
                options.append(option)
                
    except Exception as e:
        logger.warning(f"Error extracting bus options: {e}")

    return options
