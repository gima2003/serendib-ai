import logging
from typing import List
from agents.planner.route.schemas import (
    RouteRequest, RouteResponse, RouteSummary, RouteLegResult, Coordinate
)
from agents.planner.route.geocoding_service import geocode_location
from agents.planner.route.routing_service import get_route
from agents.planner.route.road_context_service import get_road_context
from agents.planner.route.bus_route_service import get_bus_options
from agents.planner.route.scenic_route_service import get_scenic_places_near_route
from agents.planner.route.route_scoring import calculate_route_score

logger = logging.getLogger(__name__)

async def route_plan(request: RouteRequest) -> RouteResponse:
    """
    Coordinates the Route workflow:
    1. Geocode locations
    2. Determine legs
    3. Call routing API
    4. Enrich with road dataset, bus, scenic
    5. Score route
    """
    destinations = request.destinations
    if len(destinations) < 2:
        raise ValueError("At least 2 destinations (start and end) are required.")

    legs_results = []
    total_dist = 0.0
    total_time = 0.0

    # Geocode all locations
    coordinates_map = {}
    for loc in destinations:
        coord = await geocode_location(loc)
        if not coord:
            raise ValueError(f"Could not geocode location: {loc}")
        coordinates_map[loc] = coord

    # Process each leg
    for i in range(len(destinations) - 1):
        origin_name = destinations[i]
        dest_name = destinations[i+1]
        
        origin_coord = coordinates_map[origin_name]
        dest_coord = coordinates_map[dest_name]
        
        logger.info(f"Processing leg: {origin_name} to {dest_name}")
        
        # 1. Routing
        road_route = await get_route(origin_coord, dest_coord, mode="drive")
        if road_route:
            total_dist += road_route.distance_km
            total_time += road_route.estimated_duration_minutes
            
        # 2. Road context
        road_context = get_road_context(origin_coord, dest_coord)
        
        # 3. Bus Options
        bus_options = get_bus_options(origin_name, dest_name)
        
        # 4. Scenic Places
        scenic_places = get_scenic_places_near_route(origin_coord, dest_coord)
        
        # 5. Scoring
        score = calculate_route_score(
            road_route=road_route,
            bus_options=bus_options,
            scenic_places=scenic_places,
            travel_style=request.travel_style,
            interests=[] # We can pull interests from traveller_profile in the future
        )
        
        leg_result = RouteLegResult(
            from_location=origin_name,
            to_location=dest_name,
            coordinates={
                "origin": origin_coord,
                "destination": dest_coord
            },
            road_route=road_route,
            road_context=road_context,
            bus_options=bus_options,
            scenic_places=scenic_places,
            route_score=score
        )
        
        legs_results.append(leg_result)

    summary = RouteSummary(
        start_location=destinations[0],
        destinations=destinations[1:],
        total_distance_km=round(total_dist, 2),
        total_estimated_duration_minutes=round(total_time, 2)
    )

    return RouteResponse(
        trip_id=request.trip_id,
        route_summary=summary,
        legs=legs_results
    )
