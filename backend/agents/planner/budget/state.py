from typing import TypedDict, List, Dict, Any, Optional

class BudgetState(TypedDict, total=False):
    """
    LangGraph State definition for the Budget Agent.
    
    Fields:
    - trip_id: Unique identifier for the trip.
    - initial_budget_lkr: The original budget amount provided by the user.
    - available_budget_lkr: Calculated available budget after deductions or standardizations.
    - cost_breakdown: Segregated costs for transport, accommodation, food, attractions, and contingency.
    - estimated_total_cost_lkr: The grand total calculated for the entire trip.
    - remaining_budget_lkr: The difference between available budget and estimated total cost.
    - budget_utilization_percent: The percentage of the budget consumed by the trip.
    - within_budget: Boolean flag indicating if the trip is affordable given the user's budget.
    - transport_comparison: Alternative transport options and their estimated costs.
    - recommended_transport: The most optimal transport mode based on cost and preference.
    - savings_opportunities: Actionable tips to reduce costs (e.g., cheaper transport or food alternatives).
    - warnings: Budget-specific alerts (e.g., "Insufficient funds for chosen activities").
    - data_sources: Datasets utilized for financial calculations.
    - status: Lifecycle status of the budget agent execution (e.g., 'pending', 'completed', 'error').
    - error_message: Reason for failure if status is 'error'.
    
    Data Producer:
    - The Budget Agent consumes Route Agent outputs and user profile/food/accommodation inputs to populate these financial fields.
    
    Future Consumer:
    - The Final Planner Node (or UI Orchestrator) uses `estimated_total_cost_lkr`, `within_budget`, and `savings_opportunities` to finalize the overarching trip itinerary.
    
    Why needed for LangGraph:
    - Isolates all financial and cost-based states in a single cohesive dictionary, ensuring the downstream nodes have a reliable, strongly-typed format to evaluate if the trip is financially viable before committing to it.
    """
    
    # Inputs
    trip_id: str
    initial_budget_lkr: float
    
    # Outputs
    available_budget_lkr: Optional[float]
    cost_breakdown: Optional[Dict[str, float]]
    estimated_total_cost_lkr: Optional[float]
    remaining_budget_lkr: Optional[float]
    budget_utilization_percent: Optional[float]
    within_budget: Optional[bool]
    transport_comparison: Optional[List[Dict[str, Any]]]
    recommended_transport: Optional[Dict[str, Any]]
    savings_opportunities: Optional[List[Dict[str, Any]]]
    warnings: Optional[List[str]]
    data_sources: Optional[List[str]]
    
    # Execution Metadata
    status: str
    error_message: Optional[str]
