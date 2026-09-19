from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from agents.planner.route.schemas import RouteRequest, RouteResponse
from agents.planner.route.route_orchestrator import route_plan

from agents.planner.budget.schemas import Member1Profile, Member2Destinations, Member3FoodAcc, BudgetResponse
from agents.planner.budget.budget_orchestrator import budget_plan

router = APIRouter(prefix="/api/planner", tags=["Planner"])

class BudgetRequest(BaseModel):
    profile: Member1Profile
    destinations: Member2Destinations
    food_acc: Member3FoodAcc
    route_response: RouteResponse

@router.post("/route", response_model=RouteResponse)
async def generate_route_plan(request: RouteRequest):
    """
    Generate a route plan given a set of destinations and traveler preferences.
    Integrates geocoding, routing, road context, bus fares, and scenic places.
    """
    try:
        response = await route_plan(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during route planning.")

@router.post("/budget", response_model=BudgetResponse)
async def generate_budget_plan(request: BudgetRequest):
    """
    Generate a budget plan.
    """
    try:
        response = await budget_plan(
            request.profile,
            request.destinations,
            request.food_acc,
            request.route_response
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

