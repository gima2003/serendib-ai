from langgraph.graph import StateGraph, START, END
from state import TripState
from .nodes import (
    process_profile,
    process_destination,
    process_food,
    process_accommodation,
    process_route,
    process_budget,
    process_safety,
    process_context,
    process_schedule
)
from .nodes.replan_nodes import (
    budget_replan_node,
    safety_replan_node,
    context_replan_node
)
from .decisions import (
    route_after_budget,
    route_after_safety,
    route_after_context
)

def build_graph() -> StateGraph:
    """
    Builds the LangGraph orchestration layer for Serendib AI.
    It strictly routes the TripState sequentially through the specialist wrappers.
    """
    workflow = StateGraph(TripState)

    # 1. Add nodes
    workflow.add_node("profile_node", process_profile)
    workflow.add_node("destination_node", process_destination)
    workflow.add_node("food_node", process_food)
    workflow.add_node("accommodation_node", process_accommodation)
    workflow.add_node("route_node", process_route)
    workflow.add_node("budget_node", process_budget)
    workflow.add_node("safety_node", process_safety)
    workflow.add_node("context_node", process_context)
    workflow.add_node("schedule_node", process_schedule)
    
    # Replan nodes
    workflow.add_node("budget_replan_node", budget_replan_node)
    workflow.add_node("safety_replan_node", safety_replan_node)
    workflow.add_node("context_replan_node", context_replan_node)

    # 2. Add edges
    workflow.add_edge(START, "profile_node")
    workflow.add_edge("profile_node", "destination_node")
    workflow.add_edge("destination_node", "food_node")
    workflow.add_edge("food_node", "accommodation_node")
    workflow.add_edge("accommodation_node", "route_node")
    workflow.add_edge("route_node", "budget_node")
    
    # Budget decision
    workflow.add_conditional_edges(
        "budget_node",
        route_after_budget
    )
    workflow.add_edge("budget_replan_node", "budget_node")
    
    # Safety decision
    workflow.add_conditional_edges(
        "safety_node",
        route_after_safety
    )
    workflow.add_edge("safety_replan_node", "route_node")
    
    # Context decision
    workflow.add_conditional_edges(
        "context_node",
        route_after_context
    )
    workflow.add_edge("context_replan_node", "context_node")
    
    # Schedule
    workflow.add_edge("schedule_node", END)

    # 3. Compile the graph
    app = workflow.compile()
    return app
