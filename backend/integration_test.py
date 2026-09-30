import json
import asyncio
import os
import sys

# Mock pymongo to prevent DNS crash in test environment
import sys
from unittest.mock import MagicMock
sys.modules['pymongo'] = MagicMock()
sys.modules['pymongo.mongo_client'] = MagicMock()
sys.modules['pymongo.server_api'] = MagicMock()

# Mock geocoder to prevent Geoapify API rate limits/disconnects during test
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

from schemas.destination_schemas import DestinationPreferences
from services.destination.destination_recommender import recommend_from_traveller_profile
from services.food_agent.food_agent_service import recommend_food_places
from agents.accommodation.schemas import AccommodationRequest, StayRequest, BudgetRequest
from agents.accommodation.accommodation_service import process_accommodation_request

from routes.planner_routes import generate_trip, GenerateTripRequest
from agents.planner.budget.schemas import Member1Profile, Member2Destinations, Member3FoodAcc

# Add mock outputs representing Agent 1 extraction from:
# "I am a couple travelling from Colombo for 5 days. We want a relaxed trip focused on nature, photography, local food and culture. Our total budget is 100,000 LKR. We would like to visit Kandy, Nuwara Eliya and Ella. We prefer comfortable but reasonably priced accommodation, vegetarian food, and we want to avoid very crowded places and unnecessarily long journeys."
agent1_state = {
    "status": "ready",
    "profile": {
        "trip_id": "TRIP-FINAL-VAL",
        "duration_days": 5,
        "traveller_count": 2,
        "travel_type": "couple",
        "starting_location": "Colombo",
        "start_date": "2026-11-01",
        "end_date": "2026-11-05",
        "budget": {
            "amount": 100000,
            "currency": "LKR",
            "scope": "total_trip",
            "flexibility": "moderate"
        },
        "interests": [{"name": "nature", "preference": "high"}, {"name": "photography", "preference": "high"}, {"name": "culture", "preference": "high"}],
        "dietary_requirements": ["vegetarian"],
        "food_preferences": ["local_food"],
        "travel_pace": "relaxed",
        "crowd_preference": "avoid",
        "preferred_destinations": ["Kandy", "Nuwara Eliya", "Ella"],
        "must_visit_destinations": ["Kandy", "Nuwara Eliya", "Ella"],
        "avoidances": ["crowded places", "long road journeys"],
        "accessibility_requirements": [],
        "additional_requests": ["comfortable but reasonably priced accommodation"]
    }
}

async def run_integration_test():
    print("--- STARTING INTEGRATION TEST ---")
    
    # 1. Agent 2 (Destination)
    print("Running Agent 2 (Destination)...")
    dest_result = recommend_from_traveller_profile(
        agent1_state["profile"],
        top_destinations=3,
        top_attractions=3,
        debug=False
    )
    recommended_destinations = dest_result["recommended_destinations"]
    print(f"Destinations output: {[d['destination'] for d in recommended_destinations]}")

    # 2. Agent 3 (Food and Accommodation)
    print("Running Agent 3 (Food and Accommodation)...")
    cities = [d["destination"] for d in recommended_destinations]
    
    # Schedule Agent is missing, so we mock nights per city
    total_days = agent1_state["profile"]["duration_days"]
    days_per_city = total_days // max(1, len(cities))
    stays = []
    for c in cities:
        stays.append(StayRequest(city=c, nights=days_per_city))
        
    acc_req = AccommodationRequest(
        traveller_count=agent1_state["profile"]["traveller_count"],
        travel_type=agent1_state["profile"]["travel_type"],
        travel_pace=agent1_state["profile"]["travel_pace"],
        interests=[i["name"] for i in agent1_state["profile"]["interests"]],
        budget=BudgetRequest(
            amount=agent1_state["profile"]["budget"]["amount"],
            currency=agent1_state["profile"]["budget"]["currency"]
        ),
        stays=stays
    )
    
    acc_response = process_accommodation_request(acc_req)
    print("Accommodation generation successful")

    food_recommendations = []
    for c in cities:
        res = recommend_food_places(
            city=c,
            budget="moderate",
            dietary="vegetarian",
            prefer_local=True,
            limit=3
        )
        if res.get("recommendations"):
            for r in res["recommendations"]:
                # mapping to FoodRecommendation expected by budget
                food_recommendations.append({
                    "estimated_cost_per_person_lkr": 2000.0 # hardcoded because price_band_lkr is a string
                })

    print(f"Food generation successful")
    
    acc_recs = []
    for plan in acc_response.accommodation_plan:
        for opt in plan.hotel_options:
            acc_recs.append({
                "accommodation_id": opt.accommodation_id,
                "name": opt.name,
                "city": opt.city,
                "estimated_cost_per_night_lkr": opt.price_information.estimated_price_per_night_lkr or 15000,
                "required_rooms": 1,
                "recommended_nights": plan.nights,
                "is_selected": opt.is_selected
            })

    # Prepare for Agent 4
    food_acc = {
        "food_recommendations": food_recommendations,
        "accommodation_recommendations": acc_recs
    }

    # Format profile for generate_trip
    profile_dict = agent1_state["profile"].copy()
    profile_dict["travellers"] = {"adults": profile_dict["traveller_count"], "children": 0}
    
    print("Running Agent 4 (Planner via generate_trip)...")
    try:
        gen_trip_req = GenerateTripRequest(
            profile=profile_dict,
            destinations=recommended_destinations,
            food_acc=food_acc
        )
        trip_response = await generate_trip(gen_trip_req)
        print("--- TRIP GENERATED SUCCESSFULLY ---")
        print("Budget Utilization:", trip_response.budget_plan.budget_utilization_percent, "%")
        
        print("Running Schedule Agent...")
        from agents.planner.schedule.schedule_service import generate_schedule
        from agents.planner.schedule.schemas import ScheduleAgentRequest
        
        from models.traveller_profile import TravellerProfile
        profile_obj = TravellerProfile(**profile_dict)
        
        schedule_req = ScheduleAgentRequest(
            profile=profile_obj,
            destinations=recommended_destinations,
            stays=acc_response.accommodation_plan,
            food_options=[], # Mock empty for integration test since format differs slightly
            route_plan=trip_response.route_plan,
            budget_plan=trip_response.budget_plan,
            safety_plan=trip_response.safety_plan,
            context_plan=trip_response.context_plan
        )
        schedule_response = await generate_schedule(schedule_req)
        print("--- SCHEDULE GENERATED SUCCESSFULLY ---")
        print(f"Total itinerary days: {len(schedule_response.itinerary)}")
        if len(schedule_response.itinerary) > 0:
            print(f"First day city: {schedule_response.itinerary[0].city}")
        print(f"Warnings: {schedule_response.overall_warnings}")
        
        # Save output
        os.makedirs("test_outputs", exist_ok=True)
        with open("test_outputs/final_trip_plan.json", "w") as f:
            f.write(schedule_response.model_dump_json(indent=2))
        print("Saved final trip plan to test_outputs/final_trip_plan.json")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("ERROR:", str(e))

if __name__ == "__main__":
    asyncio.run(run_integration_test())
