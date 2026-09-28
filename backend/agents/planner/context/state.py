from typing import TypedDict, List, Dict, Any, Optional

class ContextState(TypedDict, total=False):
    """
    LangGraph State definition for the Context Agent.
    
    Fields:
    - trip_id: Unique identifier for the trip.
    - crowd_predictions: List of daily predictions mapping locations to crowd scores, levels, and rules triggered.
    - weather_predictions: List of daily weather contexts mapping locations to rain probability and activity impacts.
    - context_alerts: High-priority unified alerts (e.g., 'Rain may affect hiking', 'High crowd due to Poya').
    - context_warnings: Generic context-related warnings for the trip.
    - recommendations: Aggregated suggestions based on crowd and weather heuristics.
    - status: Lifecycle status of the context agent execution (e.g., 'pending', 'completed', 'error').
    - error_message: Reason for failure if status is 'error'.
    
    Data Producer:
    - The Context Agent evaluates the user's travel dates and intended destinations against the Sri Lankan holiday calendar and weather APIs to populate these fields.
    
    Future Consumer:
    - The UI presentation layer consumes `crowd_predictions` and `context_alerts` to display timeline-based context to the user.
    - Future multi-agent orchestrator layers may use `context_alerts` to perform localized activity swaps (e.g., swapping a hike for a museum on a rainy day).
    
    Why needed for LangGraph:
    - Encapsulates non-critical but highly impactful travel intelligence. By holding this in a standard graph state, other nodes (like Budget or Route) don't have to duplicate calendar checking logic, and the final compiler node can inject rich context into the final trip itinerary.
    """
    
    # Inputs
    trip_id: str
    
    # Outputs
    crowd_predictions: Optional[List[Dict[str, Any]]]
    weather_predictions: Optional[List[Dict[str, Any]]]
    context_alerts: Optional[List[Dict[str, Any]]]
    context_warnings: Optional[List[str]]
    recommendations: Optional[List[str]]
    
    # Execution Metadata
    status: str
    error_message: Optional[str]
