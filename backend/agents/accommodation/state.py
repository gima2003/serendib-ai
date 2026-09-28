from typing import TypedDict, List, Dict, Any, Optional
from agents.accommodation.schemas import (
    AccommodationRequest,
    AccommodationCandidate,
    DestinationAccommodation,
    AccommodationResponse
)

class AccommodationState(TypedDict):
    request: AccommodationRequest
    candidates_by_city: Dict[str, List[AccommodationCandidate]]
    normalized_candidates: Dict[str, List[AccommodationCandidate]]
    accommodation_plan: List[DestinationAccommodation]
    response: Optional[AccommodationResponse]
    metadata: Dict[str, Any]
    limitations: List[str]
    errors: List[str]
