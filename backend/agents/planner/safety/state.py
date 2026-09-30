from typing import TypedDict, List, Dict, Any, Optional

class SafetyState(TypedDict, total=False):
    """
    LangGraph State definition for the Safety Agent.
    
    Fields:
    - trip_id: Unique identifier for the trip.
    - route_safety_score: A calculated score (0-100) representing the overall safety of the route.
    - risk_level: Categorized risk severity (e.g., 'LOW', 'MEDIUM', 'HIGH').
    - route_segments: Segment-by-segment safety evaluation including from/to locations, scores, and risk levels.
    - safety_explanation: Rule-based explanations for why a specific risk level was assigned.
    - weather_summary: Captured weather conditions for the destination/route during the travel dates.
    - hazard_summary: Results from scanning landslide or environmental hazard zones.
    - incident_summary: Count and details of historical incidents near the travel path.
    - warnings: Critical safety alerts demanding user attention.
    - recommendations: Safe travel recommendations based on detected risks.
    - replanning_required: Boolean flag indicating if the trip is too dangerous and must be replanned.
    - replanning_actions: Suggested steps to take if replanning is forced.
    - data_sources: Origins of the safety data (e.g., LHMP, OpenWeather).
    - status: Lifecycle status of the safety agent execution (e.g., 'pending', 'completed', 'error').
    - error_message: Reason for failure if status is 'error'.
    
    Data Producer:
    - The Safety Agent analyzes the Route Agent's paths and User activities against static hazard rules to populate these fields.
    
    Future Consumer:
    - A future Dynamic Trip Replanning graph node will consume `replanning_required` and `risk_level` to conditionally loop back and request the Route Agent to generate an alternative path.
    
    Why needed for LangGraph:
    - This state serves as the conditional routing mechanism in LangGraph. By exposing `replanning_required` globally, the graph router can dynamically decide whether to proceed to completion or trigger an automated trip rewrite.
    """
    
    # Inputs
    trip_id: str
    
    # Outputs
    route_safety_score: Optional[int]
    risk_level: Optional[str]
    route_segments: Optional[List[Dict[str, Any]]]
    safety_explanation: Optional[List[str]]
    weather_summary: Optional[Dict[str, Any]]
    hazard_summary: Optional[Dict[str, Any]]
    incident_summary: Optional[Dict[str, Any]]
    warnings: Optional[List[str]]
    recommendations: Optional[List[str]]
    replanning_required: Optional[bool]
    replanning_actions: Optional[List[str]]
    data_sources: Optional[List[str]]
    
    # Execution Metadata
    status: str
    error_message: Optional[str]
