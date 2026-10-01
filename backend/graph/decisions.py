from typing import Literal

from state import TripState
from agents.planner.budget.schemas import BudgetResponse
from agents.planner.safety.schemas import SafetyResponse
from agents.planner.context.schemas import ContextResponse

MAX_BUDGET_REPLAN_ATTEMPTS = 2
MAX_SAFETY_REPLAN_ATTEMPTS = 2
MAX_CONTEXT_REPLAN_ATTEMPTS = 1

def route_after_budget(state: TripState) -> Literal["safety_node", "budget_replan_node"]:
    """
    Decides whether to proceed to Safety or Replan Budget.
    """
    budget_plan: BudgetResponse = state.get("budget_plan")
    attempts = state.get("budget_replan_attempts", 0)
    
    if not budget_plan:
        return "safety_node"
        
    if budget_plan.within_budget:
        return "safety_node"
        
    if attempts >= MAX_BUDGET_REPLAN_ATTEMPTS:
        return "safety_node"
        
    # Check if last decision was to stop replanning
    history = state.get("decision_history", [])
    if history and history[-1].get("agent") == "budget" and history[-1].get("decision") == "stop_replanning":
        return "safety_node"
        
    return "budget_replan_node"

def route_after_safety(state: TripState) -> Literal["context_node", "safety_replan_node"]:
    """
    Decides whether to proceed to Context or Replan Route based on Safety.
    """
    safety_plan: SafetyResponse = state.get("safety_plan")
    attempts = state.get("safety_replan_attempts", 0)
    
    if not safety_plan:
        return "context_node"
        
    if not safety_plan.replanning_required:
        return "context_node"
        
    if attempts >= MAX_SAFETY_REPLAN_ATTEMPTS:
        return "context_node"
        
    history = state.get("decision_history", [])
    if history and history[-1].get("agent") == "safety" and history[-1].get("decision") == "stop_replanning":
        return "context_node"
        
    return "safety_replan_node"

def route_after_context(state: TripState) -> Literal["schedule_node", "context_replan_node"]:
    """
    Decides whether to proceed to Schedule or Replan based on Context.
    """
    context_plan: ContextResponse = state.get("context_plan")
    attempts = state.get("context_replan_attempts", 0)
    
    if not context_plan:
        return "schedule_node"
        
    # Check if there are significant alerts
    if not context_plan.context_alerts:
        return "schedule_node"
        
    if attempts >= MAX_CONTEXT_REPLAN_ATTEMPTS:
        return "schedule_node"
        
    history = state.get("decision_history", [])
    if history and history[-1].get("agent") == "context" and history[-1].get("decision") == "stop_replanning":
        return "schedule_node"
        
    return "context_replan_node"
