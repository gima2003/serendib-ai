from typing import List, Dict, Any

def check_replanning(risk_level: str, weather_condition: str, activities: List[str]) -> Dict[str, Any]:
    replanning_required = False
    suggestions = []
    
    if risk_level == "HIGH":
        replanning_required = True
        suggestions.append("Select safer attractions")
        
        weather_cond_lower = weather_condition.lower()
        if "rain" in weather_cond_lower or "storm" in weather_cond_lower or "shower" in weather_cond_lower:
            suggestions.append("Move outdoor attractions to another day")
            
        outdoor_keywords = ["hiking", "trekking", "camping", "outdoor"]
        is_outdoor = any(any(kw in act.lower() for kw in outdoor_keywords) for act in activities)
        
        if is_outdoor:
            suggestions.append("Delay hiking activities")
            suggestions.append("Travel during daytime")
            
    return {
        "replanning_required": replanning_required,
        "suggestions": suggestions
    }
