import requests
import json

payload = {
    "origin": "",
    "start_date": "2026-11-03",
    "end_date": "2026-11-08",
    "traveller_count": 2,
    "traveller_type": "couple",
    "interests": ["nature", "photography", "mountains", "waterfalls", "local culture", "authentic sri lankan food"],
    "travel_pace": "relaxed",
    "crowd_preference": "avoid",
    "preferred_regions": ["Kandy", "Nuwara Eliya", "Ella"],
    "additional_notes": "relaxing journey without rushing too much",
    "budget": {
        "amount": 100000,
        "currency": "LKR",
        "flexibility": "moderate"
    },
    "travel_style": "mid-range",
    "accommodation_preferences": ["eco lodges", "hotels"],
    "transport_preferences": [],
    "dietary_preference": "Vegetarian",
    "food_preferences": ["Authentic Sri Lankan food"],
    "selected_activities": []
}

resp = requests.post("http://127.0.0.1:8002/profile/guided", json=payload)
print(resp.status_code)
print(resp.text)
