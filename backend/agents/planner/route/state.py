from typing import TypedDict, List, Dict, Any, Optional

class RouteState(TypedDict, total=False):
    """
    LangGraph State definition for the Route Agent.
    
    Fields:
    - trip_id: Unique identifier for the trip.
    - request_destinations: Ordered list of destinations provided by the user.
    - travel_style: User's preferred travel style (e.g., moderate).
    - transport_preferences: List of transport modes (e.g., car, bus).
    - budget_level: High-level budget preference for routing (e.g., moderate).
    - route_summary: High-level summary including start location, total distance, and duration.
    - legs: Detailed route segments containing from/to locations, coordinates, road routes, bus options, and scenic places.
    - data_sources: List of APIs and datasets used (e.g., Geoapify, OSM).
    - limitations: Known limitations of the generated route plan.
    - status: Lifecycle status of the route agent execution (e.g., 'pending', 'completed', 'error').
    - error_message: Reason for failure if status is 'error'.
    
    Data Producer:
    - The Route Agent populates `route_summary`, `legs`, `data_sources`, and `limitations` after executing its deterministic geocoding and routing logic.
    
    Future Consumer:
    - The Budget Agent uses `legs` to calculate transport costs.
    - The Safety Agent uses `legs` (specifically the coordinates) to perform hazard and incident checks along the path.
    
    Why needed for LangGraph:
    - Decouples the route generation process so that its output can be cleanly passed down the graph to dependent nodes (Budget and Safety) without tightly coupling the agent functions.
    """
    
    # Inputs
    trip_id: str
    request_destinations: List[str]
    travel_style: Optional[str]
    transport_preferences: Optional[List[str]]
    budget_level: Optional[str]
    
    # Outputs
    route_summary: Optional[Dict[str, Any]]
    legs: Optional[List[Dict[str, Any]]]
    data_sources: Optional[List[str]]
    limitations: Optional[List[str]]
    
    # Execution Metadata
    status: str
    error_message: Optional[str]
