import logging
import pandas as pd
from typing import List, Dict, Any
from agents.planner.budget.schemas import TransportOption
from agents.planner.route.schemas import RouteResponse

logger = logging.getLogger(__name__)

def calculate_transport_options(
    route_response: RouteResponse,
    train_df: pd.DataFrame,
    taxi_df: pd.DataFrame,
    total_travellers: int,
    travel_style: str
) -> List[TransportOption]:
    """
    Calculates cost options for valid transport modes supported by data.
    """
    options = []
    
    # 1. Bus
    bus_option = _calculate_bus(route_response, total_travellers)
    if bus_option:
        options.append(bus_option)
        
    # 2. Train
    train_option = _calculate_train(route_response, train_df, total_travellers, travel_style)
    if train_option:
        options.append(train_option)
        
    # 3. Taxi/Rental
    taxi_options = _calculate_taxi(route_response, taxi_df)
    options.extend(taxi_options)
    
    return options

def _calculate_bus(route_response: RouteResponse, total_travellers: int) -> TransportOption:
    """Calculates bus cost based on Route V1 valid bus_options, evaluated per leg."""
    if not route_response.legs:
        return TransportOption(mode="bus", price_available=False, coverage="unavailable", reason=["No route legs provided."])
        
    total_bus_fare = 0.0
    legs_priced = 0
    total_legs = len(route_response.legs)
    breakdown = {"legs": []}
    
    for leg in route_response.legs:
        valid_buses = [b for b in leg.bus_options if b.fare_valid and b.fare_lkr is not None and b.fare_lkr > 0]
        
        if valid_buses:
            cheapest_bus = min(valid_buses, key=lambda b: b.fare_lkr)
            total_bus_fare += cheapest_bus.fare_lkr
            legs_priced += 1
            breakdown["legs"].append({
                "from": leg.from_location,
                "to": leg.to_location,
                "fare": cheapest_bus.fare_lkr,
                "available": True
            })
        else:
            breakdown["legs"].append({
                "from": leg.from_location,
                "to": leg.to_location,
                "fare": 0.0,
                "available": False
            })
            
    coverage = "complete" if legs_priced == total_legs else ("partial" if legs_priced > 0 else "unavailable")
    price_available = (coverage == "complete")
    
    total_cost = total_bus_fare * total_travellers
    return TransportOption(
        mode="bus",
        estimated_cost_lkr=total_cost,
        price_available=price_available,
        coverage=coverage,
        reason=[f"Bus pricing is {coverage} ({legs_priced}/{total_legs} legs priced)."],
        breakdown={"fare_per_person": total_bus_fare, "total_travellers": total_travellers, "legs_info": breakdown["legs"]}
    )

def _calculate_train(route_response: RouteResponse, train_df: pd.DataFrame, total_travellers: int, travel_style: str) -> TransportOption:
    """
    Calculates train cost evaluated per leg.
    The dataset explicitly supports fares from Colombo, so we only price legs connected to Colombo.
    """
    if train_df.empty:
        return TransportOption(mode="train", price_available=False, coverage="unavailable", reason=["Train dataset missing."])
        
    if not route_response.legs:
        return TransportOption(mode="train", price_available=False, coverage="unavailable", reason=["No route legs provided."])
        
    total_train_fare = 0.0
    legs_priced = 0
    total_legs = len(route_response.legs)
    breakdown = {"legs": []}
    colombo_variants = ["colombo", "colombo fort"]
    
    for leg in route_response.legs:
        start_loc = leg.from_location.lower()
        end_loc = leg.to_location.lower()
        
        is_start_colombo = any(v in start_loc for v in colombo_variants)
        is_end_colombo = any(v in end_loc for v in colombo_variants)
        
        target_station = None
        if is_start_colombo and not is_end_colombo:
            target_station = end_loc
        elif is_end_colombo and not is_start_colombo:
            target_station = start_loc
            
        leg_fare = 0.0
        leg_available = False
        
        if target_station:
            station_match = train_df[train_df['Station'].str.lower().str.contains(target_station, na=False)]
            if not station_match.empty:
                row = station_match.iloc[0]
                if row['fare_valid']:
                    fare_col = '2nd_Class_Rs'
                    if travel_style == 'luxury':
                        fare_col = '1st_Class_Rs'
                    elif travel_style == 'budget':
                        fare_col = '3rd_Class_Rs'
                        
                    if pd.isna(row.get(fare_col)) or row.get(fare_col) <= 0:
                        for fallback_col in ['2nd_Class_Rs', '3rd_Class_Rs', '1st_Class_Rs']:
                            if not pd.isna(row.get(fallback_col)) and row.get(fallback_col) > 0:
                                fare_col = fallback_col
                                break
                                
                    per_person_fare = row.get(fare_col)
                    if not pd.isna(per_person_fare) and per_person_fare > 0:
                        leg_fare = float(per_person_fare)
                        leg_available = True

        if leg_available:
            total_train_fare += leg_fare
            legs_priced += 1
            breakdown["legs"].append({
                "from": leg.from_location,
                "to": leg.to_location,
                "fare": leg_fare,
                "available": True
            })
        else:
            breakdown["legs"].append({
                "from": leg.from_location,
                "to": leg.to_location,
                "fare": 0.0,
                "available": False
            })
            
    coverage = "complete" if legs_priced == total_legs else ("partial" if legs_priced > 0 else "unavailable")
    price_available = (coverage == "complete")
    
    total_cost = total_train_fare * total_travellers
    return TransportOption(
        mode="train",
        estimated_cost_lkr=total_cost,
        price_available=price_available,
        coverage=coverage,
        reason=[f"Train pricing is {coverage} ({legs_priced}/{total_legs} legs priced)."],
        breakdown={"fare_per_person": total_train_fare, "total_travellers": total_travellers, "legs_info": breakdown["legs"]}
    )

def _calculate_taxi(route_response: RouteResponse, taxi_df: pd.DataFrame) -> List[TransportOption]:
    """
    Evaluates taxi/rental options.
    Returns price_available=False because "included km" semantics are unverified,
    preserving the available data.
    """
    options = []
    
    if taxi_df.empty:
        return options
        
    distance_km = route_response.route_summary.total_distance_km
    
    for _, row in taxi_df.iterrows():
        provider = row.get('provider', 'Unknown')
        mode = row.get('mode', 'rental')
        
        # If the mode is rental, we do not invent a base_fare * duration formula.
        # We preserve the values but mark as unavailable for exact computation.
        
        base_fare = row.get('base_fare')
        per_km = row.get('per_km')
        pricing_valid = row.get('pricing_valid', False)
        
        if not pricing_valid or row.get('availability') == 'on_request':
            options.append(TransportOption(
                mode="taxi",
                provider=provider,
                price_available=False,
                reason=["Pricing is 'on_request' or invalid in dataset."]
            ))
            continue
            
        options.append(TransportOption(
            mode="taxi",
            provider=provider,
            price_available=False, # As requested: do not compute unless semantics verified
            reason=["Base fare and per_km semantics (e.g. daily included mileage) are unverified. Cannot compute exact trip price."],
            breakdown={"raw_base_fare": base_fare, "raw_per_km": per_km, "route_distance_km": distance_km}
        ))
        
    return options
