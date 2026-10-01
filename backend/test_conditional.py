import asyncio
import sys
import os

from graph.graph import build_graph

# Mocks
from unittest.mock import MagicMock
sys.modules['pymongo'] = MagicMock()
sys.modules['pymongo.mongo_client'] = MagicMock()
sys.modules['pymongo.server_api'] = MagicMock()
sys.modules['pymongo.saslprep'] = MagicMock()

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

from models.traveller_profile import TravellerProfile, TravelType, TravelPace, Interest, Budget
import datetime

def get_base_profile(amount: float):
    return TravellerProfile(
        trip_id="TRIP-REPLAN",
        duration_days=5,
        traveller_count=2,
        travel_type=TravelType.couple,
        travel_pace=TravelPace.relaxed,
        starting_location="Colombo",
        start_date=datetime.date(2026, 11, 1),
        interests=[Interest(name="nature"), Interest(name="photography")],
        dietary_requirements=["vegetarian"],
        budget=Budget(amount=amount, currency="LKR"),
        must_visit=["Kandy", "Nuwara Eliya", "Ella"],
        avoid=[],
        accessibility_requirements=[]
    )

async def test_over_budget():
    print("\n--- STARTING OVER BUDGET SCENARIO ---")
    app = build_graph()
    
    initial_state = {
        "trip_id": "TRIP-REPLAN-BUDGET",
        "status": "started",
        "errors": [],
        "warnings": [],
        "budget_replan_attempts": 0,
        "safety_replan_attempts": 0,
        "context_replan_attempts": 0,
        "decision_history": [],
        "raw_user_request": "",
        "profile": get_base_profile(1000.0) # Very low budget
    }
    
    final_state = await app.ainvoke(initial_state)
    
    print("--- EXECUTION COMPLETED ---")
    print(f"Decision History: {final_state.get('decision_history')}")
    print(f"Budget Replan Attempts: {final_state.get('budget_replan_attempts')}")
    if final_state.get('budget_plan'):
        print(f"Final Within Budget: {final_state['budget_plan'].within_budget}")
    
async def test_normal_trip():
    print("\n--- STARTING NORMAL TRIP SCENARIO ---")
    app = build_graph()
    
    initial_state = {
        "trip_id": "TRIP-NORMAL",
        "status": "started",
        "errors": [],
        "warnings": [],
        "budget_replan_attempts": 0,
        "safety_replan_attempts": 0,
        "context_replan_attempts": 0,
        "decision_history": [],
        "raw_user_request": "",
        "profile": get_base_profile(500000.0) # High budget
    }
    
    final_state = await app.ainvoke(initial_state)
    
    print("--- EXECUTION COMPLETED ---")
    print(f"Decision History (should be empty): {final_state.get('decision_history')}")
    print(f"Budget Replan Attempts: {final_state.get('budget_replan_attempts')}")
    if final_state.get('budget_plan'):
        print(f"Final Within Budget: {final_state['budget_plan'].within_budget}")

async def main():
    await test_normal_trip()
    await test_over_budget()

if __name__ == "__main__":
    asyncio.run(main())
