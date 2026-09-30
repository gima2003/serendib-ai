import json
from agents.planner.schedule.schemas import ScheduleAgentRequest, ScheduleResponse
from agents.planner.schedule.schedule_builder import build_itinerary
from models.traveller_profile import TravellerProfile
from agents.accommodation.schemas import DestinationAccommodation, AccommodationRecommendationResult, AccommodationPriceInfo
from agents.planner.budget.schemas import BudgetResponse, CostBreakdown, RecommendedTransport
from agents.planner.route.schemas import RouteResponse, RouteSummary
from agents.planner.safety.schemas import SafetyResponse
from agents.planner.context.schemas import ContextResponse

def test_build_schedule():
    req = ScheduleAgentRequest(
        profile=TravellerProfile(trip_id="TRIP-1", duration_days=3, traveller_count=2),
        destinations=[
            {"city": "Kandy", "attractions": [{"name": "Temple"}, {"name": "Lake"}]},
            {"city": "Ella", "attractions": [{"name": "Ella Rock"}]}
        ],
        stays=[
            DestinationAccommodation(
                city="Kandy", nights=2, 
                hotel_options=[AccommodationRecommendationResult(accommodation_id="1", name="Kandy Hotel", city="Kandy", source="test", is_selected=True, price_information=AccommodationPriceInfo())]
            ),
            DestinationAccommodation(
                city="Ella", nights=1, 
                hotel_options=[AccommodationRecommendationResult(accommodation_id="2", name="Ella Hotel", city="Ella", source="test", is_selected=True, price_information=AccommodationPriceInfo())]
            )
        ],
        food_options=[],
        route_plan=RouteResponse(
            trip_id="TRIP-1", 
            route_summary=RouteSummary(start_location="Colombo", destinations=["Kandy", "Ella"], total_distance_km=100, total_estimated_duration_minutes=120),
            legs=[]
        ),
        budget_plan=BudgetResponse(
            trip_id="TRIP-1",
            available_budget_lkr=100000,
            cost_breakdown=CostBreakdown(transport_lkr=0, accommodation_lkr=0, food_lkr=0, attractions_lkr=0, contingency_lkr=0),
            subtotal_cost_lkr=10000,
            estimated_total_cost_lkr=11000,
            remaining_budget_lkr=89000,
            budget_utilization_percent=11.0,
            within_budget=True,
            highest_expense_category="transport",
            highest_expense_percentage=0.0,
            transport_comparison=[],
            recommended_transport=RecommendedTransport(recommended_mode="car", estimated_cost_lkr=0),
            savings_opportunities=[],
            warnings=[]
        ),
        safety_plan=SafetyResponse(
            trip_id="TRIP-1", route_safety_score=100, risk_level="Low", route_segments=[], safety_explanation=[],
            weather_summary={}, hazard_summary={}, incident_summary={}, warnings=[], recommendations=[], replanning_required=False,
            replanning_actions=[], data_sources=[]
        ),
        context_plan=ContextResponse(
            trip_id="TRIP-1", crowd_predictions=[], weather_predictions=[], context_alerts=[], context_warnings=[], recommendations=[]
        )
    )

    resp = build_itinerary(req)
    assert resp.status == "completed"
    assert len(resp.itinerary) == 3
    
    assert resp.itinerary[0].city == "Kandy"
    assert resp.itinerary[1].city == "Kandy"
    assert resp.itinerary[2].city == "Ella"
    
    print("Schedule test passed!")
    
if __name__ == "__main__":
    test_build_schedule()
