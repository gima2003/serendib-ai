from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List

from agents.planner.route.schemas import RouteRequest, RouteResponse
from agents.planner.route.route_orchestrator import route_plan

from agents.planner.budget.schemas import Member1Profile, Member2Destinations, Member3FoodAcc, BudgetResponse
from agents.planner.budget.budget_orchestrator import budget_plan

from agents.planner.safety.schemas import SafetyResponse
from agents.planner.safety.safety_orchestrator import safety_plan

from agents.planner.context.schemas import ContextResponse
from agents.planner.context.context_orchestrator import context_plan

router = APIRouter(prefix="/api/planner", tags=["Planner"])

class BudgetRequest(BaseModel):
    profile: Member1Profile
    destinations: Member2Destinations
    food_acc: Member3FoodAcc
    route_response: RouteResponse

class AgentGenericRequest(BaseModel):
    profile: dict
    destinations: list
    route_response: dict

class GenerateTripRequest(BaseModel):
    profile: dict
    destinations: list
    food_acc: dict

class GenerateTripResponse(BaseModel):
    route_plan: RouteResponse
    budget_plan: BudgetResponse
    safety_plan: SafetyResponse
    context_plan: ContextResponse

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

@router.post("/safety", response_model=SafetyResponse)
async def generate_safety_plan(request: AgentGenericRequest):
    """
    Generate a safety plan for the given destinations and route.
    """
    try:
        response = await safety_plan(request.profile, request.destinations, request.route_response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/context", response_model=ContextResponse)
async def generate_context_plan(request: AgentGenericRequest):
    """
    Generate a context plan involving weather and crowd predictions.
    """
    try:
        response = await context_plan(request.profile, request.destinations, request.route_response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-trip", response_model=GenerateTripResponse)
async def generate_trip(request: GenerateTripRequest):
    """
    Master endpoint that runs Route -> Budget -> Safety -> Context agents sequentially.
    """
    try:
        # 1. Route Agent
        route_destinations = [d.get("city", d.get("location", "")) for d in request.destinations]
        route_req = RouteRequest(
            trip_id=request.profile.get("trip_id", "TRIP-1"),
            destinations=route_destinations,
            travel_style=request.profile.get("travel_style", "moderate"),
            transport_preferences=request.profile.get("transport_preferences", ["car"]),
            budget_level=request.profile.get("budget_level", "moderate")
        )
        route_resp = await route_plan(route_req)
        
        # 2. Budget Agent
        budget_resp = await budget_plan(
            Member1Profile(**request.profile),
            Member2Destinations(destinations=request.destinations),
            Member3FoodAcc(**request.food_acc),
            route_resp
        )
        
        # 3. Safety Agent
        safety_resp = await safety_plan(
            request.profile, 
            request.destinations, 
            route_resp.model_dump()
        )
        
        # 4. Context Agent
        context_resp = await context_plan(
            request.profile, 
            request.destinations, 
            route_resp.model_dump()
        )
        
        return GenerateTripResponse(
            route_plan=route_resp,
            budget_plan=budget_resp,
            safety_plan=safety_resp,
            context_plan=context_resp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during trip generation: {str(e)}")

