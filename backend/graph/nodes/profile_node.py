import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from state import TripState
from llm.prompts import build_profile_prompt
from llm.llm_service import extract_traveller_profile

logger = logging.getLogger(__name__)

async def process_profile(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node that acts as a thin wrapper around Agent 1 (Profile Extraction).
    Reads 'raw_user_request' from state and updates 'profile'.
    Also auto-computes end_date from start_date + duration_days when missing.
    """
    logger.info("Executing Profile Node")
    
    raw_request = state.get("raw_user_request")
    if not raw_request:
        # If no raw request but profile already set (Guided Planner path), keep it
        existing_profile = state.get("profile")
        if existing_profile:
            logger.info("Profile already set via Guided Planner — computing dates if missing.")
            return _ensure_dates(existing_profile)
        logger.warning("No raw_user_request provided, skipping profile extraction.")
        return {}
        
    try:
        # Re-use existing prompt builder
        prompt = build_profile_prompt(raw_request)
        
        # Re-use existing service call
        profile = extract_traveller_profile(prompt)
        
        return _ensure_dates(profile)
    except Exception as e:
        logger.error(f"Error in Profile Node: {str(e)}")
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Profile extraction failed: {str(e)}"]}


def _ensure_dates(profile) -> Dict[str, Any]:
    """
    If profile has start_date but no end_date, compute end_date = start_date + duration_days.
    Also ensures start_date is ISO-formatted if already set.
    """
    updates: Dict[str, Any] = {"profile": profile}
    
    start_date = getattr(profile, "start_date", None)
    end_date = getattr(profile, "end_date", None)
    duration_days = getattr(profile, "duration_days", None)
    
    if start_date and not end_date and duration_days:
        try:
            s = datetime.strptime(start_date[:10], "%Y-%m-%d")
            e = s + timedelta(days=int(duration_days) - 1)
            profile.end_date = e.strftime("%Y-%m-%d")
            logger.info(f"Auto-computed end_date: {profile.end_date} from start={start_date}, duration={duration_days}")
        except (ValueError, TypeError) as ex:
            logger.warning(f"Could not compute end_date: {ex}")
    
    return updates
