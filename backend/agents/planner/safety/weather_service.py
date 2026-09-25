import os
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def _fallback_weather() -> Dict[str, Any]:
    return {
        "rain_probability": 0,
        "temperature": 28,
        "weather_condition": "clear"
    }

def get_weather_forecast(latitude: float, longitude: float, travel_date: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return _fallback_weather()
        
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "list" in data and len(data["list"]) > 0:
            first_forecast = data["list"][0]
            temp = first_forecast.get("main", {}).get("temp", 28)
            pop = first_forecast.get("pop", 0) * 100
            weather_desc = first_forecast.get("weather", [{}])[0].get("description", "clear")
            
            return {
                "rain_probability": int(pop),
                "temperature": round(temp),
                "weather_condition": weather_desc.lower()
            }
    except Exception as e:
        logger.error(f"Weather API failed: {e}")
        
    return _fallback_weather()
