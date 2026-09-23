import asyncio
import json
import logging
from pathlib import Path

from agents.planner.budget.schemas import Member1Profile, Member2Destinations, Member3FoodAcc
from agents.planner.route.schemas import RouteResponse
from agents.planner.budget.budget_orchestrator import budget_plan

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MOCK_DIR = BASE_DIR / "data" / "planner" / "mock"

async def main():
    logger.info("Running Budget development mock...")
    
    # 1. Load Mocks
    with open(MOCK_DIR / "member1_profile.json", "r") as f:
        profile_data = json.load(f)
    
    with open(MOCK_DIR / "member2_destinations.json", "r") as f:
        dest_data = json.load(f)
        
    with open(MOCK_DIR / "member3_food.json", "r") as f:
        food_data = json.load(f)
        
    profile = Member1Profile(**profile_data)
    destinations = Member2Destinations(**dest_data)
    food_acc = Member3FoodAcc(**food_data)
    
    # 2. Construct a mock Route V1 output that matches schemas.py
    route_mock = {
        "trip_id": profile.trip_id,
        "route_summary": {
            "start_location": "Colombo",
            "destinations": ["Kandy", "Ella"],
            "total_distance_km": 240.0,
            "total_estimated_duration_minutes": 360.0
        },
        "legs": [
            {
                "from_location": "Colombo",
                "to_location": "Kandy",
                "coordinates": {},
                "bus_options": [
                    {
                        "route_number": "1",
                        "route_id": "col-kdy",
                        "from_location": "Colombo",
                        "to_location": "Kandy",
                        "fare_lkr": 500.0,
                        "fare_valid": True
                    }
                ],
                "route_score": {"total": 0.9, "breakdown": {}}
            },
            {
                "from_location": "Kandy",
                "to_location": "Ella",
                "coordinates": {},
                "bus_options": [
                    {
                        "route_number": "2",
                        "route_id": "kdy-ela",
                        "from_location": "Kandy",
                        "to_location": "Ella",
                        "fare_lkr": 700.0,
                        "fare_valid": True
                    }
                ],
                "route_score": {"total": 0.8, "breakdown": {}}
            }
        ],
        "data_sources": [],
        "limitations": []
    }
    
    route_response = RouteResponse(**route_mock)
    
    # 3. Call Orchestrator
    try:
        response = await budget_plan(profile, destinations, food_acc, route_response)
        print("\n--- FINAL BUDGET RESPONSE ---")
        print(response.model_dump_json(indent=2))
    except Exception as e:
        logger.exception(f"Budget mock failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
