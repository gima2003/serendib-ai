import json
import asyncio
from agents.accommodation.schemas import AccommodationRequest, BudgetRequest, StayRequest
from agents.accommodation.accommodation_service import process_accommodation_request

async def run_mock():
    request = AccommodationRequest(
        traveller_count=2,
        travel_type="couple",
        travel_pace="relaxed",
        interests=["nature", "photography"],
        budget=BudgetRequest(amount=900.0, currency="USD"),
        stays=[
            StayRequest(city="Kandy", nights=2),
            StayRequest(city="Nuwara Eliya", nights=1),
            StayRequest(city="Ella", nights=1)
        ]
    )
    
    response = process_accommodation_request(request)
    print(json.dumps(response.model_dump(), indent=2))

if __name__ == "__main__":
    asyncio.run(run_mock())
