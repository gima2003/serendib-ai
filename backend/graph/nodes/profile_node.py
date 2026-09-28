import logging
from typing import Dict, Any

from state import TripState
from llm.prompts import build_profile_prompt
from llm.llm_service import extract_traveller_profile

logger = logging.getLogger(__name__)

async def process_profile(state: TripState) -> Dict[str, Any]:
    """
    LangGraph node that acts as a thin wrapper around Agent 1 (Profile Extraction).
    Reads 'raw_user_request' from state and updates 'profile'.
    """
    logger.info("Executing Profile Node")
    
    raw_request = state.get("raw_user_request")
    if not raw_request:
        logger.warning("No raw_user_request provided, skipping profile extraction.")
        return {}
        
    try:
        # Re-use existing prompt builder
        prompt = build_profile_prompt(raw_request)
        
        # Re-use existing service call
        profile = extract_traveller_profile(prompt)
        
        return {"profile": profile}
    except Exception as e:
        logger.error(f"Error in Profile Node: {str(e)}")
        # Do not swallow errors; pass them into the state
        current_errors = state.get("errors", [])
        return {"errors": current_errors + [f"Profile extraction failed: {str(e)}"]}
