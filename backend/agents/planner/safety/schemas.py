from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SafetyResponse(BaseModel):
    trip_id: str
    route_safety_score: int
    risk_level: str
    route_segments: List[Dict[str, Any]]
    safety_explanation: List[str]
    weather_summary: Dict[str, Any]
    hazard_summary: Dict[str, Any]
    incident_summary: Dict[str, Any]
    warnings: List[str]
    recommendations: List[str]
    replanning_required: bool
    replanning_actions: List[str]
    data_sources: List[str]
