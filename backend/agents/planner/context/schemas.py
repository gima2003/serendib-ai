from pydantic import BaseModel
from typing import List

class CrowdPrediction(BaseModel):
    date: str
    location: str
    crowd_score: int
    crowd_level: str
    reasons: List[str]
    recommendations: List[str]

class WeatherPrediction(BaseModel):
    location: str
    temperature: float
    rain_probability: int
    weather_condition: str
    activity_impact: str
    recommendations: List[str]

class ContextAlert(BaseModel):
    type: str
    date: str | None = None
    location: str | None = None
    message: str

class ContextResponse(BaseModel):
    trip_id: str
    crowd_predictions: List[CrowdPrediction]
    weather_predictions: List[WeatherPrediction]
    context_alerts: List[ContextAlert]
    context_warnings: List[str]
    recommendations: List[str]
