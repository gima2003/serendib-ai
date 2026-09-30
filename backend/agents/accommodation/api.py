from fastapi import APIRouter, HTTPException
from agents.accommodation.schemas import AccommodationRequest, AccommodationResponse
from agents.accommodation.accommodation_service import process_accommodation_request

router = APIRouter(prefix="/api/planner/accommodation", tags=["Accommodation"])

@router.post("/", response_model=AccommodationResponse)
async def generate_accommodation_plan(request: AccommodationRequest):
    """
    Standalone endpoint for Accommodation Agent.
    """
    try:
        response = process_accommodation_request(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
