import asyncio
import sys

from state import TripState
from graph.nodes import (
    process_profile,
    process_destination,
    process_food,
    process_accommodation,
    process_route,
    process_budget,
    process_safety,
    process_context,
    process_schedule
)

# Mock pymongo to prevent DNS crash in test environment
from unittest.mock import MagicMock
sys.modules['pymongo'] = MagicMock()
sys.modules['pymongo.mongo_client'] = MagicMock()
sys.modules['pymongo.server_api'] = MagicMock()
sys.modules['pymongo.saslprep'] = MagicMock()

# Mock Geoapify mapping limits
import agents.planner.route.geocoding_service as geocoder_module
from agents.planner.route.schemas import Coordinate
async def mock_geocode_location(*args, **kwargs):
    return Coordinate(latitude=6.9, longitude=79.8)
geocoder_module.geocode_location = mock_geocode_location

import agents.planner.route.routing_service as routing_module
from agents.planner.route.schemas import RoadRouteData
async def mock_get_route(*args, **kwargs):
    return RoadRouteData(
        distance_km=100.0,
        estimated_duration_minutes=120,
        route_path=[],
        polyline="",
        mode="drive"
    )
routing_module.get_route = mock_get_route

async def main():
    print("Testing LangGraph Node Wrappers...")
    
    state: TripState = {
        "trip_id": "test-id",
        "status": "ready",
        "errors": [],
        "warnings": [],
        "raw_user_request": "I am a couple travelling from Colombo for 5 days. We want a relaxed trip focused on nature, photography, local food and culture. Our total budget is 100,000 LKR. We would like to visit Kandy, Nuwara Eliya and Ella.",
        "profile": None,
        "destinations": [],
        "food_options": [],
        "accommodation_plan": None,
        "stays": [],
        "route_plan": None,
        "budget_plan": None,
        "safety_plan": None,
        "context_plan": None,
        "schedule_plan": None
    }
    
    # 1. Profile Node
    res = await process_profile(state)
    state.update(res)
    print(f"Profile: {state['profile'] is not None}")
    
    # 2. Destination Node
    res = await process_destination(state)
    state.update(res)
    print(f"Destinations count: {len(state['destinations'])}")
    
    # 3. Food Node
    res = await process_food(state)
    state.update(res)
    print(f"Food Options count: {len(state['food_options'])}")
    
    # 4. Accommodation Node
    res = await process_accommodation(state)
    state.update(res)
    print(f"Accommodation Plan: {state['accommodation_plan'] is not None}")
    
    # 5. Route Node
    res = await process_route(state)
    state.update(res)
    print(f"Route Plan: {state['route_plan'] is not None}")
    
    # 6. Budget Node
    res = await process_budget(state)
    state.update(res)
    print(f"Budget Plan: {state['budget_plan'] is not None}")
    
    # 7. Safety Node
    res = await process_safety(state)
    state.update(res)
    print(f"Safety Plan: {state['safety_plan'] is not None}")
    
    # 8. Context Node
    res = await process_context(state)
    state.update(res)
    print(f"Context Plan: {state['context_plan'] is not None}")
    
    # 9. Schedule Node
    res = await process_schedule(state)
    state.update(res)
    print(f"Schedule Plan: {state['schedule_plan'] is not None}")
    
    print("\nErrors:", state["errors"])

if __name__ == "__main__":
    asyncio.run(main())
