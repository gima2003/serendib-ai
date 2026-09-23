import asyncio
import json
import logging
from unittest.mock import patch
from agents.planner.route.schemas import RouteRequest, Coordinate, RoadRouteData
from agents.planner.route.route_orchestrator import route_plan
from database.core.config import GEOAPIFY_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_with_mocks(request: RouteRequest):
    logger.info("Running with mocked Geoapify APIs since API key is missing.")
    
    colombo_coord = Coordinate(latitude=6.9271, longitude=79.8612)
    kandy_coord = Coordinate(latitude=7.2906, longitude=80.6337)
    ella_coord = Coordinate(latitude=6.8667, longitude=81.0466)
    
    async def mock_geo(loc):
        if "Colombo" in loc: return colombo_coord
        if "Kandy" in loc: return kandy_coord
        if "Ella" in loc: return ella_coord
        return Coordinate(latitude=7.0, longitude=80.0)
        
    async def mock_rt(orig, dest, mode):
        return RoadRouteData(
            distance_km=115.0,
            estimated_duration_minutes=180.0,
            mode=mode,
            instructions=["Head straight", "Turn left"]
        )

    with patch('backend.agents.planner.route.route_orchestrator.geocode_location', side_effect=mock_geo):
        with patch('backend.agents.planner.route.route_orchestrator.get_route', side_effect=mock_rt):
            response = await route_plan(request)
            return response

async def main():
    # Mock input from Member 1 (Profile)
    member_1_mock = {
      "trip_id": "TRIP001",
      "travel_style": "moderate",
      "transport_preferences": ["train", "bus"]
    }
    
    # Mock input from Member 2 (Destinations)
    member_2_mock = {
      "destinations": [
        {"city": "Colombo"},
        {"city": "Kandy"},
        {"city": "Ella"}
      ]
    }
    
    destinations = [d["city"] for d in member_2_mock["destinations"]]
    
    request = RouteRequest(
        trip_id=member_1_mock["trip_id"],
        destinations=destinations,
        travel_style=member_1_mock["travel_style"],
        transport_preferences=member_1_mock["transport_preferences"]
    )
    
    try:
        if not GEOAPIFY_API_KEY:
            response = await run_with_mocks(request)
        else:
            logger.info("Executing real route orchestrator...")
            response = await route_plan(request)
            
        logger.info("Orchestrator finished successfully!")
        
        print("\n--- FINAL ROUTE RESPONSE ---")
        print(response.model_dump_json(indent=2))
        
    except Exception as e:
        logger.error(f"Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
