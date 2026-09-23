import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import json
import asyncio
from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

payload = {
  "profile": {
    "trip_id": "TRIP-MOCK-123",
    "start_date": "2026-09-24",
    "end_date": "2026-09-28",
    "travel_date": "2026-09-26",
    "duration_days": 5,
    "travel_style": "moderate",
    "transport_preferences": ["bus", "train", "car"],
    "activities": ["hiking", "sightseeing"],
    "travellers": {
      "adults": 2,
      "children": 0
    },
    "budget": {
      "amount": 100000,
      "currency": "LKR"
    }
  },
  "destinations": [
    {
      "city": "Kandy",
      "location": "Kandy",
      "category": "popular",
      "latitude": 7.2906,
      "longitude": 80.6337,
      "attractions": [
        {
          "name": "Temple of the Tooth",
          "estimated_entry_cost_lkr": 2000
        }
      ]
    },
    {
      "city": "Ella",
      "location": "Ella",
      "category": "popular",
      "latitude": 6.8667,
      "longitude": 81.0466,
      "attractions": [
        {
          "name": "Nine Arches Bridge",
          "estimated_entry_cost_lkr": 0
        }
      ]
    }
  ],
  "food_acc": {
    "food_recommendations": [
      {
        "estimated_cost_per_person_lkr": 3000
      }
    ],
    "accommodation_recommendations": [
      {
        "estimated_cost_per_night_lkr": 8000,
        "recommended_nights": 4
      }
    ]
  }
}

print("Executing POST /api/planner/generate-trip...")
response = client.post("/api/planner/generate-trip", json=payload)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(response.text)
