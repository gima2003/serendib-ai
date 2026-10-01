from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime

from graph.graph import build_graph
from models.traveller_profile import TravellerProfile
from database.core.database import db
from security.auth_security import get_current_user
from services.subscription_guard import (
    check_guided_plan_access,
    increment_guided_plan_usage,
)

router = APIRouter(prefix="/api/trips", tags=["Trips"])

class GenerateTripRequest(BaseModel):
    raw_user_request: Optional[str] = None
    traveller_profile: Optional[Dict[str, Any]] = None

class SaveTripRequest(BaseModel):
    trip_data: Dict[str, Any]

def serialize_mongo(doc):
    if not doc: return doc
    doc["_id"] = str(doc["_id"])
    return doc

@router.post("")
async def save_trip(request: SaveTripRequest, current_user: dict = Depends(get_current_user)):
    """Save a generated trip to MongoDB."""
    trip = request.trip_data
    
    trip["user_id"] = str(current_user["_id"])
    trip["status"] = "UPCOMING"
    trip["saved"] = True
    trip["created_at"] = datetime.utcnow()
    trip["updated_at"] = trip["created_at"]
    
    # Extract trip name from profile
    profile = trip.get("profile") or {}
    if isinstance(profile, dict):
        trip["trip_name"] = profile.get("trip_name", "Sri Lanka Escape")
    else:
        trip["trip_name"] = "Sri Lanka Escape"

    try:
        # All values from /generate are already serialized dicts (via _to_dict).
        # Just make sure any remaining Pydantic objects are also serialized.
        def _ensure_dict(obj):
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            return obj
        
        # Ensure consistent key naming: accept both old format (food, accommodation, route, ...)
        # and new format (food_options, accommodation_plan, route_plan, ...)
        # Normalize to new _plan format
        if "food" in trip and "food_options" not in trip:
            trip["food_options"] = trip.pop("food")
        if "accommodation" in trip and "accommodation_plan" not in trip:
            trip["accommodation_plan"] = trip.pop("accommodation")
        if "route" in trip and "route_plan" not in trip:
            trip["route_plan"] = trip.pop("route")
        if "budget" in trip and "budget_plan" not in trip:
            trip["budget_plan"] = trip.pop("budget")
        if "safety" in trip and "safety_plan" not in trip:
            trip["safety_plan"] = trip.pop("safety")
        if "context" in trip and "context_plan" not in trip:
            trip["context_plan"] = trip.pop("context")
        if "schedule" in trip and "schedule_plan" not in trip:
            trip["schedule_plan"] = trip.pop("schedule")
            
        result = await db.trips.insert_one(trip)
        trip["_id"] = str(result.inserted_id)
        return trip
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def get_user_trips(current_user: dict = Depends(get_current_user)):
    """Get all trips for current user."""
    trips_cursor = db.trips.find({"user_id": str(current_user["_id"])}).sort("created_at", -1)
    trips = await trips_cursor.to_list(length=100)
    return [serialize_mongo(t) for t in trips]

@router.get("/recommendations")
async def get_recommendations(current_user: dict = Depends(get_current_user)):
    """Get Agent 2 recommendations based on user profile if available, else generic."""
    # We can fetch the user's latest trip to get their profile, or just use a dummy profile to spin up Agent 2.
    latest_trip = await db.trips.find_one({"user_id": str(current_user["_id"])}, sort=[("created_at", -1)])
    
    from services.destination.destination_recommender import recommend_from_traveller_profile
    
    if latest_trip and latest_trip.get("profile"):
        profile_dict = latest_trip["profile"]
    else:
        profile_dict = {
            "travel_type": "Couple",
            "budget_level": "Mid-range",
            "pace": "Moderate",
            "interests": ["Nature", "Culture", "Beaches"]
        }
        
    try:
        dest_result = recommend_from_traveller_profile(
            profile_dict,
            top_destinations=3,
            top_attractions=3,
            debug=False
        )
        
        destinations = dest_result.get("recommended_destinations", [])
        
        # Format for frontend
        recs = []
        for i, dest in enumerate(destinations[:3]):
            # Depending on how it's structured, attractions might be objects or dicts
            attractions = dest.get("attractions", [])
            tags = [a.get("type", "Sightseeing") for a in attractions[:2]] if len(attractions) > 0 and isinstance(attractions[0], dict) else ["Nature", "Culture"]
            
            recs.append({
                "id": i + 1,
                "title": dest.get("city", dest.get("destination", "Unknown")),
                "tags": tags,
                "match": dest.get("match_score", 80),
                "image": dest.get("city", dest.get("destination", "unknown")).lower()
            })
        return recs
    except Exception as e:
        # Fallback if Agent 2 fails
        return [
            { "id": 1, "title": "Ella", "tags": ["Nature", "Hiking"], "match": 92, "image": "ella" },
            { "id": 2, "title": "Kandy", "tags": ["Culture", "Nature"], "match": 89, "image": "kandy" },
            { "id": 3, "title": "Galle", "tags": ["Beach", "Heritage"], "match": 86, "image": "galle" },
        ]

@router.get("/upcoming")
async def get_upcoming_trip(current_user: dict = Depends(get_current_user)):
    """Get the closest upcoming trip."""
    trip = await db.trips.find_one(
        {"user_id": str(current_user["_id"]), "status": "UPCOMING"},
        sort=[("created_at", -1)]
    )
    return serialize_mongo(trip) if trip else None

@router.get("/{trip_id}")
async def get_trip(trip_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific trip."""
    trip = await db.trips.find_one({"trip_id": trip_id, "user_id": str(current_user["_id"])})
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return serialize_mongo(trip)

@router.patch("/{trip_id}/cancel")
async def cancel_trip(trip_id: str, current_user: dict = Depends(get_current_user)):
    """Cancel a specific trip if it is UPCOMING."""
    user_id_str = str(current_user["_id"])
    trip = await db.trips.find_one({"trip_id": trip_id, "user_id": user_id_str})
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    if trip.get("status") != "UPCOMING":
        raise HTTPException(status_code=400, detail="Only UPCOMING trips can be cancelled")
        
    update_result = await db.trips.update_one(
        {"trip_id": trip_id, "user_id": user_id_str},
        {"$set": {
            "status": "CANCELLED",
            "cancelled_at": datetime.utcnow()
        }}
    )
    
    if update_result.modified_count == 1:
        updated_trip = await db.trips.find_one({"trip_id": trip_id, "user_id": user_id_str})
        return serialize_mongo(updated_trip)
    else:
        raise HTTPException(status_code=500, detail="Failed to cancel trip")

@router.post("/generate")
async def generate_trip_langgraph(
    request: GenerateTripRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Master endpoint that runs the entire Serendib AI LangGraph workflow.
    """
    try:
        user_id = str(current_user["_id"])


        await check_guided_plan_access(
            user_id
        )

        app = build_graph()
        
        trip_id = f"TRIP-{uuid.uuid4().hex[:8].upper()}"
        
        initial_state = {
            "trip_id": trip_id,
            "status": "started",
            "errors": [],
            "warnings": [],
            "budget_replan_attempts": 0,
            "safety_replan_attempts": 0,
            "context_replan_attempts": 0,
            "decision_history": [],
            "raw_user_request": request.raw_user_request or "",
        }
        
        if request.traveller_profile:
            # The Guided Planner gives us a pre-built profile.
            initial_state["profile"] = TravellerProfile(**request.traveller_profile)
            
        final_state = await app.ainvoke(initial_state)
        
        def _to_dict(obj):
            """Recursively serialize Pydantic models and nested structures, fixing JSON non-compliant floats."""
            import math
            if obj is None:
                return None
            if isinstance(obj, float):
                if math.isnan(obj) or math.isinf(obj):
                    return 0.0
                return obj
            if hasattr(obj, "model_dump"):
                return _to_dict(obj.model_dump())
            if isinstance(obj, list):
                return [_to_dict(item) for item in obj]
            if isinstance(obj, dict):
                return {k: _to_dict(v) for k, v in obj.items()}
            return obj
        
        # Log summary for debugging
        profile_obj = final_state.get("profile")
        schedule_obj = final_state.get("schedule_plan")
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"GENERATE COMPLETE: trip_id={trip_id}")
        logger.info(f"  Profile: duration={getattr(profile_obj, 'duration_days', None)} days, type={getattr(profile_obj, 'travel_type', None)}")
        logger.info(f"  Destinations: {[d.get('city') or d.get('destination') for d in (final_state.get('destinations') or [])]}")
        logger.info(f"  Schedule days: {len(schedule_obj.itinerary) if schedule_obj else 0}")
        logger.info(f"  Errors: {final_state.get('errors')}")

        await increment_guided_plan_usage(
            user_id
        )
        
        return {
            "trip_id": trip_id,
            # Use consistent _plan suffix keys so TripWorkspace can read them uniformly
            "profile": _to_dict(final_state.get("profile")),
            "destinations": _to_dict(final_state.get("destinations")),
            "food_options": _to_dict(final_state.get("food_options")),
            "accommodation_plan": _to_dict(final_state.get("accommodation_plan")),
            "route_plan": _to_dict(final_state.get("route_plan")),
            "budget_plan": _to_dict(final_state.get("budget_plan")),
            "safety_plan": _to_dict(final_state.get("safety_plan")),
            "context_plan": _to_dict(final_state.get("context_plan")),
            "schedule_plan": _to_dict(final_state.get("schedule_plan")),
            "errors": final_state.get("errors"),
            "warnings": final_state.get("warnings"),
        }
    except Exception as e:
        import logging, traceback
        logging.getLogger(__name__).error(f"Generate trip failed: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error generating trip: {str(e)}")
