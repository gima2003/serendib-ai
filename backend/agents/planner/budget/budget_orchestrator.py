import logging
from typing import Dict, Any

from agents.planner.route.schemas import RouteResponse
from agents.planner.budget.schemas import (
    Member1Profile, Member2Destinations, Member3FoodAcc,
    CostBreakdown, BudgetResponse
)
from agents.planner.budget.data_loader import load_train_prices, load_taxi_rates
from agents.planner.budget.trip_cost_service import calculate_trip_costs
from agents.planner.budget.transport_cost_service import calculate_transport_options
from agents.planner.budget.budget_scoring import recommend_transport
from agents.planner.budget.budget_optimizer import find_savings_opportunities

logger = logging.getLogger(__name__)

async def budget_plan(
    profile: Member1Profile,
    destinations: Member2Destinations,
    food_acc: Member3FoodAcc,
    route_response: RouteResponse
) -> BudgetResponse:
    """
    Main orchestration logic for the Budget Agent (Member 4).
    Calculates costs across all categories, evaluates transport modes,
    and produces deterministic budget recommendations.
    """
    logger.info(f"Starting Budget calculation for trip {profile.trip_id}")
    
    # 1. Load Data
    # For a production application, these could be cached or passed in, 
    # but loading them cleanly here per the requirements.
    train_df = load_train_prices()
    taxi_df = load_taxi_rates()
    
    # 2. Calculate Non-Transport Costs
    acc_lkr, food_lkr, attr_lkr, warnings = calculate_trip_costs(profile, destinations, food_acc)
    
    base_non_transport = acc_lkr + food_lkr + attr_lkr
    
    # 3. Calculate Transport Options
    total_travellers = profile.travellers.adults + profile.travellers.children
    
    transport_options = calculate_transport_options(
        route_response=route_response,
        train_df=train_df,
        taxi_df=taxi_df,
        total_travellers=total_travellers,
        travel_style=profile.travel_style
    )
    
    # 4. Determine Recommended Transport
    available_budget = profile.budget.amount
    if profile.budget.currency == "USD":
        available_budget *= 300.0  # minimum required fix for conversion
        
    remaining_budget_for_transport = available_budget - base_non_transport
    
    recommendation = recommend_transport(
        transport_options=transport_options,
        preferences=profile.transport_preferences,
        remaining_budget_for_transport=remaining_budget_for_transport
    )
    
    # 5. Finalize Costs with Contingency
    subtotal = base_non_transport + recommendation.estimated_cost_lkr
    contingency_cost = subtotal * 0.10
    estimated_total_cost = subtotal + contingency_cost
    
    remaining_budget = available_budget - estimated_total_cost
    
    if available_budget > 0:
        utilization = (estimated_total_cost / available_budget) * 100.0
    else:
        utilization = 100.0 if estimated_total_cost > 0 else 0.0
        
    within_budget = remaining_budget >= 0
    
    if not within_budget:
        warnings.append("Trip exceeds available budget. Consider savings opportunities.")
    if recommendation.recommended_mode == "unknown":
        warnings.append("The complete trip cost cannot be calculated because transport pricing is incomplete.")
    
    # 6. Savings Opportunities
    selected_opt = next((opt for opt in transport_options if opt.mode == recommendation.recommended_mode), None)
    
    savings, over_budget_amount, highest_cat, highest_pct = find_savings_opportunities(
        selected_transport=selected_opt,
        transport_options=transport_options,
        estimated_total_cost_lkr=estimated_total_cost,
        available_budget_lkr=available_budget,
        acc_lkr=acc_lkr,
        food_lkr=food_lkr,
        attr_lkr=attr_lkr,
        food_acc=food_acc
    )
    
    # 7. Build Response
    cost_breakdown = CostBreakdown(
        transport_lkr=recommendation.estimated_cost_lkr,
        accommodation_lkr=acc_lkr,
        food_lkr=food_lkr,
        attractions_lkr=attr_lkr,
        contingency_lkr=contingency_cost
    )
    
    response = BudgetResponse(
        trip_id=profile.trip_id,
        available_budget_lkr=available_budget,
        cost_breakdown=cost_breakdown,
        subtotal_cost_lkr=subtotal,
        estimated_total_cost_lkr=estimated_total_cost,
        remaining_budget_lkr=remaining_budget,
        budget_utilization_percent=utilization,
        within_budget=within_budget,
        over_budget_amount=over_budget_amount,
        highest_expense_category=highest_cat,
        highest_expense_percentage=highest_pct,
        transport_comparison=transport_options,
        recommended_transport=recommendation,
        savings_opportunities=savings,
        data_sources=[
            "train_price_clean.csv",
            "taxi_rates_clean.csv",
            "Route V1 bus options",
            "Member 1, 2, 3 outputs"
        ],
        warnings=warnings
    )
    
    logger.info("Budget calculation finished successfully.")
    return response
