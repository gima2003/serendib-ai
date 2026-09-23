from datetime import datetime, timedelta
from .holiday_calendar import SRI_LANKAN_HOLIDAYS
from .schemas import CrowdPrediction

POPULAR_DESTINATIONS = [
    "ella", "nuwara eliya", "gregory lake", "ambewela farm", "kandy", "galle",
    "sigiriya", "mirissa", "yala", "arugam bay", "polonnaruwa", "anuradhapura",
    "kandy temple of tooth"
]

def is_long_weekend(date_str: str) -> bool:
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = date_obj.weekday()
    
    dates_to_check = []
    if weekday == 4: # Friday
        dates_to_check.append(date_obj)
    elif weekday == 5: # Saturday
        dates_to_check.append(date_obj - timedelta(days=1)) # Friday
        dates_to_check.append(date_obj + timedelta(days=2)) # Monday
    elif weekday == 6: # Sunday
        dates_to_check.append(date_obj - timedelta(days=2)) # Friday
        dates_to_check.append(date_obj + timedelta(days=1)) # Monday
    elif weekday == 0: # Monday
        dates_to_check.append(date_obj)
        
    for d in dates_to_check:
        d_str = d.strftime("%Y-%m-%d")
        if d_str in SRI_LANKAN_HOLIDAYS:
            return True
            
    return False

def calculate_crowd_prediction(travel_date: str, location: str, category: str = "") -> CrowdPrediction:
    date_obj = datetime.strptime(travel_date, "%Y-%m-%d")
    weekday = date_obj.weekday()
    
    score = 0
    reasons = []
    recommendations = []
    
    holiday_info = SRI_LANKAN_HOLIDAYS.get(travel_date)
    is_poya = False
    
    if holiday_info:
        reasons.append(holiday_info["name"])
        if holiday_info["type"] == "poya":
            score += 30
            is_poya = True
        elif holiday_info["type"] == "public":
            score += 40
            
    is_weekend = weekday >= 5
    if is_weekend:
        score += 20
        reasons.append("Weekend")
        
    if is_long_weekend(travel_date):
        score += 30
        reasons.append("Long weekend")
        
    is_popular = location.lower() in POPULAR_DESTINATIONS or category.lower() == "popular"
    if is_popular:
        score += 20
        reasons.append("Popular tourist area")
        
    if is_poya and (category.lower() == "religious" or "temple" in location.lower() or "kovil" in location.lower() or location.lower() == "kandy temple of tooth"):
        score += 20
        reasons.append("Religious place on Poya day")
        
    score = min(score, 100)
    
    if score <= 30:
        crowd_level = "LOW"
    elif score <= 60:
        crowd_level = "MEDIUM"
    elif score <= 80:
        crowd_level = "HIGH"
    else:
        crowd_level = "VERY_HIGH"
        
    if crowd_level in ["HIGH", "VERY_HIGH"]:
        recommendations = [
            "Visit popular attractions early morning",
            "Avoid afternoon peak hours"
        ]
    elif crowd_level == "MEDIUM":
        recommendations = [
            "Expect moderate crowds",
            "Book tickets in advance if possible"
        ]
    else:
        recommendations = [
            "Regular visiting hours are fine"
        ]
        
    return CrowdPrediction(
        date=travel_date,
        location=location,
        crowd_score=score,
        crowd_level=crowd_level,
        reasons=reasons,
        recommendations=recommendations
    )
