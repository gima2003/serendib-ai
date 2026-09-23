from typing import List, Dict
from agents.planner.route.schemas import RouteScore, RoadRouteData, BusOption, ScenicPlace

# Configurable weights for explainability
DEFAULT_WEIGHTS = {
    "travel_time": 1.0,
    "distance": 0.5,
    "scenic": 2.0,
    "cost": 1.5,
    "preference": 1.0
}

def calculate_route_score(
    road_route: RoadRouteData,
    bus_options: List[BusOption],
    scenic_places: List[ScenicPlace],
    travel_style: str = "moderate",
    interests: List[str] = None
) -> RouteScore:
    """
    Deterministic and explainable multi-criteria scoring system.
    """
    if interests is None:
        interests = []
        
    weights = DEFAULT_WEIGHTS.copy()
    
    # Adjust weights based on member 1 preferences
    if "nature" in interests or "beach" in interests:
        weights["scenic"] += 1.0
        
    if travel_style == "budget":
        weights["cost"] += 1.0
    elif travel_style == "luxury":
        weights["cost"] = 0.1 # Cost doesn't matter much
        
    breakdown: Dict[str, float] = {}
    total_score = 0.0
    
    # 1. Travel Time Score (inverse relation: less time is better, max capped at some value)
    if road_route:
        # e.g., 100 base points minus minutes/10
        time_score = max(0.0, 100.0 - (road_route.estimated_duration_minutes / 10.0))
        breakdown["travel_time_score"] = time_score * weights["travel_time"]
        
        # 2. Distance Score
        dist_score = max(0.0, 100.0 - (road_route.distance_km / 5.0))
        breakdown["distance_score"] = dist_score * weights["distance"]
    else:
        breakdown["travel_time_score"] = 0.0
        breakdown["distance_score"] = 0.0
        
    # 3. Scenic Score (based on number of places)
    scenic_score = min(100.0, len(scenic_places) * 20.0)
    breakdown["scenic_score"] = scenic_score * weights["scenic"]
    
    # 4. Cost Score (if bus is available)
    if bus_options:
        cost_score = 80.0 # Having a bus is good for cost
    else:
        cost_score = 40.0 # Standard driving cost
    breakdown["cost_score"] = cost_score * weights["cost"]
    
    # Total
    total_score = sum(breakdown.values())
    
    return RouteScore(
        total=round(total_score, 2),
        breakdown={k: round(v, 2) for k, v in breakdown.items()}
    )
