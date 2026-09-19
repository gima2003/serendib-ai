from typing import Dict, Any

def calculate_safety_score(hazard_range: int, rain_prob: int, weather_cond: str, incidents: int) -> Dict[str, Any]:
    score = 100
    
    # Hazard range rules
    if hazard_range == 4:
        score -= 30
    elif hazard_range == 3:
        score -= 20
        
    # Weather rules
    weather_cond_lower = weather_cond.lower()
    
    is_heavy_rain = ("heavy rain" in weather_cond_lower or "extreme" in weather_cond_lower 
                     or "storm" in weather_cond_lower or rain_prob > 80)
    is_medium_rain = (not is_heavy_rain and ("rain" in weather_cond_lower or 
                                             "shower" in weather_cond_lower or 
                                             rain_prob > 50))
    
    if is_heavy_rain:
        score -= 25
    elif is_medium_rain:
        score -= 10
        
    # Incident rules
    score -= (5 * incidents)
    
    # Minimum boundary
    score = max(0, score)
    
    # Risk levels
    if score >= 80:
        risk_level = "LOW"
    elif score >= 50:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
        
    return {
        "safety_score": score,
        "risk_level": risk_level
    }
