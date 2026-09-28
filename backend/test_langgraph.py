import asyncio
import sys
import json
import os

from graph.graph import build_graph

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


async def test_langgraph():
    print("--- STARTING LANGGRAPH INTEGRATION TEST ---")
    
    app = build_graph()
    
    # Realistic initial state (matches integration_test.py scenario)
    initial_state = {
        "trip_id": "TRIP-LANGGRAPH-VAL",
        "status": "started",
        "errors": [],
        "warnings": [],
        "raw_user_request": "I am a couple travelling from Colombo for 5 days. We want a relaxed trip focused on nature, photography, local food and culture. Our total budget is 100,000 LKR. We would like to visit Kandy, Nuwara Eliya and Ella. We prefer comfortable but reasonably priced accommodation, vegetarian food, and we want to avoid very crowded places and unnecessarily long journeys."
    }
    
    print("Executing Graph...")
    final_state = await app.ainvoke(initial_state)
    
    print("--- EXECUTION COMPLETED ---")
    
    # Validations
    print(f"Profile Extracted: {final_state.get('profile') is not None}")
    print(f"Destinations Count: {len(final_state.get('destinations', []))}")
    print(f"Food Options Count: {len(final_state.get('food_options', []))}")
    print(f"Accommodation Plan Present: {final_state.get('accommodation_plan') is not None}")
    print(f"Route Plan Present: {final_state.get('route_plan') is not None}")
    print(f"Budget Plan Present: {final_state.get('budget_plan') is not None}")
    print(f"Safety Plan Present: {final_state.get('safety_plan') is not None}")
    print(f"Context Plan Present: {final_state.get('context_plan') is not None}")
    print(f"Schedule Plan Present: {final_state.get('schedule_plan') is not None}")
    
    errors = final_state.get('errors', [])
    if errors:
        print(f"ERRORS DETECTED: {errors}")
    else:
        print("No errors detected.")
        
    schedule = final_state.get('schedule_plan')
    if schedule:
        print(f"Total itinerary days: {len(schedule.itinerary)}")
        if len(schedule.itinerary) > 0:
            print(f"First day city: {schedule.itinerary[0].city}")
        print(f"Budget Utilization: {final_state['budget_plan'].budget_utilization_percent}%")
        
        # Save output to compare with non-LangGraph
        os.makedirs("test_outputs", exist_ok=True)
        with open("test_outputs/langgraph_final_trip_plan.json", "w") as f:
            f.write(schedule.model_dump_json(indent=2))
        print("Saved final graph schedule output to test_outputs/langgraph_final_trip_plan.json")

if __name__ == "__main__":
    asyncio.run(test_langgraph())
