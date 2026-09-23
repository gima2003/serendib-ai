from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Coordinate(BaseModel):
    latitude: float
    longitude: float

class LocationRequest(BaseModel):
    name: str
    coordinates: Optional[Coordinate] = None

class RouteLegRequest(BaseModel):
    origin: LocationRequest
    destination: LocationRequest
    transport_modes: List[str] = Field(default_factory=lambda: ["drive"])

class RouteRequest(BaseModel):
    trip_id: str = Field(..., description="Unique trip identifier")
    destinations: List[str] = Field(..., description="Ordered list of destinations")
    travel_style: Optional[str] = "moderate"
    transport_preferences: Optional[List[str]] = Field(default_factory=lambda: ["car"])
    budget_level: Optional[str] = "moderate" # Derived from member 1

class RouteRoadContext(BaseModel):
    major_roads: List[str] = Field(default_factory=list)
    road_conditions: List[str] = Field(default_factory=list)
    closure_detected: bool = False
    districts: List[str] = Field(default_factory=list)

class BusOption(BaseModel):
    route_number: str
    route_id: str
    from_location: str
    to_location: str
    via: Optional[str] = None
    fare_lkr: Optional[float] = None
    fare_valid: bool = False

class ScenicPlace(BaseModel):
    name: str
    category: str
    latitude: float
    longitude: float
    distance_from_route_km: float
    source: str = "OSM"

class RouteScore(BaseModel):
    total: float
    breakdown: Dict[str, float]

class RoadRouteData(BaseModel):
    distance_km: float
    estimated_duration_minutes: float
    mode: str
    route_geometry: Optional[Dict[str, Any]] = None # GeoJSON LineString
    instructions: List[str] = Field(default_factory=list)

class RouteLegResult(BaseModel):
    from_location: str
    to_location: str
    coordinates: Dict[str, Coordinate] # origin, destination
    road_route: Optional[RoadRouteData] = None
    road_context: RouteRoadContext = Field(default_factory=RouteRoadContext)
    bus_options: List[BusOption] = Field(default_factory=list)
    scenic_places: List[ScenicPlace] = Field(default_factory=list)
    route_score: RouteScore

class RouteSummary(BaseModel):
    start_location: str
    destinations: List[str]
    total_distance_km: float
    total_estimated_duration_minutes: float

class RouteResponse(BaseModel):
    trip_id: str
    route_summary: RouteSummary
    legs: List[RouteLegResult]
    data_sources: List[str] = Field(default_factory=lambda: [
        "Geoapify Routing API",
        "Geoapify Geocoding API",
        "Sri Lanka Roads Dataset",
        "Bus Fare Dataset",
        "OpenStreetMap Scenic Places Dataset"
    ])
    limitations: List[str] = Field(default_factory=lambda: [
        "Train timetables are not currently integrated.",
        "Safety score and real-time traffic are not yet implemented.",
        "Bus fares might be stage-based and require manual verification if uncertain."
    ])
