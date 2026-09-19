import asyncio
import json
from .safety_orchestrator import safety_plan

async def main():
    # 1. Member 1 mock
    profile = {
        "trip_id": "TRIP-TEST-123",
        "travel_date": "2024-10-15",
        "activities": ["Outdoor hiking", "Sightseeing"]
    }
    
    # 2. Member 2 mock
    destinations = [
        {
            "name": "Ella Rock", 
            "latitude": 6.8667, 
            "longitude": 81.0466
        }
    ]
    
    # 3. Route mock
    route_response = {
        "coordinates": [
            {"lat": 6.8667, "lon": 81.0466}
        ],
        "legs": [
            {
                "from": "Colombo",
                "to": "Kandy",
                "start_location": {"lat": 6.9271, "lon": 79.8612},
                "end_location": {"lat": 7.2906, "lon": 80.6337}
            },
            {
                "from": "Kandy",
                "to": "Ella",
                "start_location": {"lat": 7.2906, "lon": 80.6337},
                "end_location": {"lat": 6.8667, "lon": 81.0466}
            }
        ]
    }
    
    print("Running Safety Agent Mock...")
    response = await safety_plan(profile, destinations, route_response)
    
    try:
        res_dict = response.model_dump()
    except AttributeError:
        res_dict = response.dict()
        
    print(json.dumps(res_dict, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
