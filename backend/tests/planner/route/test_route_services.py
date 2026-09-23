import unittest
from unittest.mock import patch, AsyncMock
import asyncio
from backend.agents.planner.route.schemas import RouteRequest, Coordinate, RoadRouteData, RouteRoadContext
from backend.agents.planner.route.route_orchestrator import route_plan

class TestRouteServices(unittest.TestCase):
    
    def setUp(self):
        self.request = RouteRequest(
            trip_id="TRIP123",
            destinations=["Colombo", "Kandy", "Ella"],
            travel_style="moderate"
        )
        
        self.colombo_coord = Coordinate(latitude=6.9271, longitude=79.8612)
        self.kandy_coord = Coordinate(latitude=7.2906, longitude=80.6337)
        self.ella_coord = Coordinate(latitude=6.8667, longitude=81.0466)

    @patch('backend.agents.planner.route.route_orchestrator.geocode_location')
    @patch('backend.agents.planner.route.route_orchestrator.get_route')
    @patch('backend.agents.planner.route.route_orchestrator.get_road_context')
    @patch('backend.agents.planner.route.route_orchestrator.get_bus_options')
    @patch('backend.agents.planner.route.route_orchestrator.get_scenic_places_near_route')
    def test_route_orchestrator_success(self, mock_scenic, mock_bus, mock_road_context, mock_route, mock_geocode):
        # Mock geocoding
        async def mock_geo(loc):
            if loc == "Colombo": return self.colombo_coord
            if loc == "Kandy": return self.kandy_coord
            if loc == "Ella": return self.ella_coord
            return None
        mock_geocode.side_effect = mock_geo
        
        # Mock routing
        async def mock_rt(orig, dest, mode):
            return RoadRouteData(
                distance_km=100.0,
                estimated_duration_minutes=120.0,
                mode=mode,
                instructions=[]
            )
        mock_route.side_effect = mock_rt
        
        # Mock sync services
        mock_road_context.return_value = RouteRoadContext(major_roads=[], road_conditions=['Good'], closure_detected=False, districts=[])
        mock_bus.return_value = []
        mock_scenic.return_value = []
        
        # Run orchestrator
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(route_plan(self.request))
        
        # Assertions
        self.assertEqual(response.trip_id, "TRIP123")
        self.assertEqual(response.route_summary.start_location, "Colombo")
        self.assertEqual(len(response.route_summary.destinations), 2)
        self.assertEqual(response.route_summary.total_distance_km, 200.0) # 2 legs * 100km
        self.assertEqual(len(response.legs), 2)
        
        leg1 = response.legs[0]
        self.assertEqual(leg1.from_location, "Colombo")
        self.assertEqual(leg1.to_location, "Kandy")
        self.assertIsNotNone(leg1.route_score)

    @patch('backend.agents.planner.route.route_orchestrator.geocode_location')
    def test_route_orchestrator_geocoding_failure(self, mock_geocode):
        async def mock_geo(loc):
            return None # Simulate failure
        mock_geocode.side_effect = mock_geo
        
        loop = asyncio.get_event_loop()
        with self.assertRaises(ValueError) as context:
            loop.run_until_complete(route_plan(self.request))
            
        self.assertIn("Could not geocode location: Colombo", str(context.exception))

if __name__ == '__main__':
    unittest.main()
