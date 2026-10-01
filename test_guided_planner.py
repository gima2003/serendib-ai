import json
from backend.models.guided_planner import GuidedPlannerRequest
from pydantic import ValidationError

payload = {
  "origin": None,
  "start_date": None,
  "end_date": None,
  "traveller_count": 2,
  "traveller_type": "friends",
  "interests": [],
  "travel_pace": "balanced",
  "crowd_preference": "neutral",
  "preferred_regions": [],
  "additional_notes": None,
  "budget": {
    "amount": None,
    "currency": "USD",
    "flexibility": "moderate"
  },
  "travel_style": "mid-range",
  "accommodation_preferences": [],
  "transport_preferences": [],
  "dietary_preference": "No restriction",
  "food_preferences": [],
  "selected_activities": []
}

try:
    req = GuidedPlannerRequest(**payload)
    print("Success")
except ValidationError as e:
    print(e.json())
