import logging
from typing import Dict, Any

from state import TripState
from agents.planner.budget.schemas import BudgetResponse
from agents.planner.safety.schemas import SafetyResponse
from agents.planner.context.schemas import ContextResponse

logger = logging.getLogger(__name__)

async def budget_replan_node(state: TripState) -> Dict[str, Any]:
    """
    Budget Replanning Node.
    Analyzes the BudgetResponse to find savings opportunities and modifies the inputs (e.g. accommodation selection).
    """
    logger.info("Executing Budget Replan Node")
    
    budget_plan = state.get("budget_plan")
    accommodation_plan = state.get("accommodation_plan")
    decision_history = state.get("decision_history", [])
    budget_attempts = state.get("budget_replan_attempts", 0)
    
    if not budget_plan or not accommodation_plan:
        return {"errors": state.get("errors", []) + ["Missing budget_plan or accommodation_plan for replanning"]}

    replan_reason = "Over budget"
    if budget_plan.highest_expense_category:
        replan_reason = f"Over budget mainly due to {budget_plan.highest_expense_category}"

    # Try to switch to a cheaper accommodation if available
    changed_accommodation = False
    new_acc_plan = accommodation_plan.model_copy(deep=True)
    
    for plan in new_acc_plan.accommodation_plan:
        selected_opt = None
        cheaper_opt = None
        for opt in plan.hotel_options:
            if opt.is_selected:
                selected_opt = opt
            elif cheaper_opt is None or opt.price_information.estimated_price_per_night_lkr < cheaper_opt.price_information.estimated_price_per_night_lkr:
                cheaper_opt = opt
                
        # If we found a selected option and a cheaper unselected option, swap them
        if selected_opt and cheaper_opt and cheaper_opt.price_information.estimated_price_per_night_lkr < selected_opt.price_information.estimated_price_per_night_lkr:
            selected_opt.is_selected = False
            cheaper_opt.is_selected = True
            changed_accommodation = True
            break # Only change one at a time

    if changed_accommodation:
        decision = {
            "agent": "budget",
            "decision": "replan_accommodation",
            "reason": replan_reason,
            "attempt": budget_attempts + 1
        }
        return {
            "accommodation_plan": new_acc_plan,
            "budget_replan_attempts": budget_attempts + 1,
            "decision_history": decision_history + [decision]
        }
    else:
        # Cannot find cheaper accommodation, or transport is the issue (transport replanning not fully implemented)
        decision = {
            "agent": "budget",
            "decision": "stop_replanning",
            "reason": "No cheaper accommodation found",
            "attempt": budget_attempts + 1
        }
        return {
            "budget_replan_attempts": budget_attempts + 1,
            "decision_history": decision_history + [decision]
        }

async def safety_replan_node(state: TripState) -> Dict[str, Any]:
    """
    Safety Replanning Node.
    Analyzes the SafetyResponse and modifies inputs (e.g. drops an unsafe destination from route).
    """
    logger.info("Executing Safety Replan Node")
    
    safety_plan = state.get("safety_plan")
    destinations = state.get("destinations", [])
    decision_history = state.get("decision_history", [])
    safety_attempts = state.get("safety_replan_attempts", 0)
    
    if not safety_plan or not destinations:
        return {"errors": state.get("errors", []) + ["Missing safety_plan or destinations for replanning"]}

    # Try dropping a destination mentioned in hazard summary or warnings
    # For now, just drop the last destination as a simple fallback, or ideally the one with issues.
    new_destinations = [d for d in destinations]
    if len(new_destinations) > 1:
        dropped = new_destinations.pop()
        dropped_name = dropped.get("city") or dropped.get("destination")
        decision = {
            "agent": "safety",
            "decision": f"drop_destination_{dropped_name}",
            "reason": f"Safety risk level: {safety_plan.risk_level}",
            "attempt": safety_attempts + 1
        }
        return {
            "destinations": new_destinations,
            "safety_replan_attempts": safety_attempts + 1,
            "decision_history": decision_history + [decision]
        }
    else:
        decision = {
            "agent": "safety",
            "decision": "stop_replanning",
            "reason": "Cannot drop the only destination",
            "attempt": safety_attempts + 1
        }
        return {
            "safety_replan_attempts": safety_attempts + 1,
            "decision_history": decision_history + [decision]
        }

async def context_replan_node(state: TripState) -> Dict[str, Any]:
    """
    Context Replanning Node.
    """
    logger.info("Executing Context Replan Node")
    
    context_plan = state.get("context_plan")
    decision_history = state.get("decision_history", [])
    context_attempts = state.get("context_replan_attempts", 0)
    
    decision = {
        "agent": "context",
        "decision": "acknowledge_warnings",
        "reason": f"Context alerts present: {len(context_plan.context_alerts)}",
        "attempt": context_attempts + 1
    }
    
    # In a real scenario, we might change dates or destinations. 
    # For now, we just acknowledge to prevent infinite loop.
    return {
        "context_replan_attempts": context_attempts + 1,
        "decision_history": decision_history + [decision]
    }
