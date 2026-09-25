import sys
import os
import json
import asyncio
from datetime import datetime, timedelta

# Add the project root to sys.path so we can import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from backend.agents.planner.context.context_orchestrator import context_plan

async def run_mock():
    # Input from Member 1
    profile = {
        "trip_id": "TRIP-MOCK-123",
        "start_date": "2026-09-24",
        "end_date": "2026-09-28"
    }
    
    # Input from Member 2
    destinations = [
        {"location": "Kandy", "category": "popular", "latitude": 7.2906, "longitude": 80.6337},
        {"location": "Ella", "category": "popular", "latitude": 6.8667, "longitude": 81.0466},
        {"location": "Nuwara Eliya", "category": "popular", "latitude": 6.9497, "longitude": 80.7839}
    ]
    
    route_response = {} # Mocked empty for now as it's not modified
    
    print("Running Context Agent Phase 2 Mock...")
    print(f"Trip: {profile['start_date']} to {profile['end_date']}")
    print("-" * 50)
    
    # Execute Context Orchestrator
    response = await context_plan(profile, destinations, route_response)
    
    print("\n--- Context Alerts (Dynamic Trip Replanning Data) ---")
    for alert in response.context_alerts:
        print(f"[{alert.date} | {alert.location}] {alert.type.upper()}: {alert.message}")
        
    print("\n--- Global Recommendations ---")
    for rec in response.recommendations:
        print(f"- {rec}")
        
    print("\n--- Raw ContextResponse Model Dump ---")
    # Using model_dump to avoid Pydantic deprecation warnings
    print(json.dumps(response.model_dump(), indent=2))

if __name__ == "__main__":
    asyncio.run(run_mock())
