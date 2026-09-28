import pytest
import pandas as pd
from agents.planner.budget.schemas import (
    Member1Profile, Member2Destinations, Member3FoodAcc, TransportOption
)
from agents.planner.route.schemas import RouteResponse
from agents.planner.budget.trip_cost_service import calculate_trip_costs
from agents.planner.budget.transport_cost_service import _calculate_bus, _calculate_train, _calculate_taxi, calculate_transport_options
from agents.planner.budget.budget_scoring import recommend_transport
from agents.planner.budget.budget_optimizer import find_savings_opportunities

def test_trip_cost_calculation():
    profile = Member1Profile(
        trip_id="T1", duration_days=2,
        travellers={"adults": 2, "children": 1},
        budget={"amount": 10000}
    ) # 3 travellers total
    
    destinations = Member2Destinations(
        destinations=[
            {"city": "Kandy", "attractions": [
                {"name": "A1", "estimated_entry_cost_lkr": 500, "cost_type": "per_person"},
                {"name": "A2", "estimated_entry_cost_lkr": 1000, "cost_type": "flat_rate"},
                {"name": "A3", "estimated_entry_cost_lkr": 200, "cost_type": "unknown"}
            ]}
        ]
    )
    
    food_acc = Member3FoodAcc(
        food_recommendations=[{"estimated_cost_per_person_lkr": 1000}],
        accommodation_recommendations=[
            {"estimated_cost_per_night_lkr": 5000, "recommended_nights": 2, "required_rooms": 2},
            {"estimated_cost_per_night_lkr": 2000, "recommended_nights": 1} # no required_rooms
        ]
    )
    
    acc_lkr, food_lkr, attr_lkr, warnings = calculate_trip_costs(profile, destinations, food_acc)
    
    # Food: 1000 * 3 = 3000
    assert food_lkr == 3000.0
    # Acc: (5000 * 2 rooms * 2 nights) + (2000 * 1 night) = 20000 + 2000 = 22000
    assert acc_lkr == 22000.0
    # Attr: A1 (500 * 3) + A2 (1000) + A3 (200) = 1500 + 1000 + 200 = 2700
    assert attr_lkr == 2700.0
    
    assert len(warnings) == 2
    assert "Room requirement not provided for accommodation unknown. Cost assumed as complete group accommodation price." in warnings
    assert "Attraction cost type unknown for 'A3'. Cost assumed as flat rate." in warnings

def test_bus_calculation_valid():
    # Setup route response mock
    route = RouteResponse(
        trip_id="T1",
        route_summary={"start_location": "A", "destinations": ["B"], "total_distance_km": 10, "total_estimated_duration_minutes": 10},
        legs=[{
            "from_location": "A", "to_location": "B",
            "coordinates": {},
            "bus_options": [{"route_number": "1", "route_id": "1", "from_location": "A", "to_location": "B", "fare_lkr": 100, "fare_valid": True}],
            "route_score": {"total": 1, "breakdown": {}}
        }],
        data_sources=[], limitations=[]
    )
    
    bus_opt = _calculate_bus(route, total_travellers=2)
    assert bus_opt is not None
    assert bus_opt.price_available is True
    assert bus_opt.coverage == "complete"
    assert bus_opt.estimated_cost_lkr == 200.0 # 100 * 2

def test_bus_calculation_invalid():
    route = RouteResponse(
        trip_id="T1",
        route_summary={"start_location": "A", "destinations": ["B"], "total_distance_km": 10, "total_estimated_duration_minutes": 10},
        legs=[
            {
                "from_location": "A", "to_location": "B",
                "coordinates": {},
                "bus_options": [{"route_number": "1", "route_id": "1", "from_location": "A", "to_location": "B", "fare_lkr": 100, "fare_valid": True}],
                "route_score": {"total": 1, "breakdown": {}}
            },
            {
                "from_location": "B", "to_location": "C",
                "coordinates": {},
                "bus_options": [{"route_number": "2", "route_id": "2", "from_location": "B", "to_location": "C", "fare_lkr": 100, "fare_valid": False}],
                "route_score": {"total": 1, "breakdown": {}}
            }
        ],
        data_sources=[], limitations=[]
    )
    bus_opt = _calculate_bus(route, 2)
    assert bus_opt.price_available is False
    assert bus_opt.coverage == "partial"

def test_train_calculation_colombo_complete():
    route = RouteResponse(
        trip_id="T1",
        route_summary={"start_location": "Colombo Fort", "destinations": ["Kandy"], "total_distance_km": 10, "total_estimated_duration_minutes": 10},
        legs=[{"from_location": "Colombo Fort", "to_location": "Kandy", "coordinates": {}, "route_score": {"total": 1, "breakdown": {}}}],
        data_sources=[], limitations=[]
    )
    
    train_df = pd.DataFrame([
        {"Station": "Kandy", "1st_Class_Rs": 1000, "2nd_Class_Rs": 500, "3rd_Class_Rs": 200, "fare_valid": True}
    ])
    
    opt = _calculate_train(route, train_df, 2, "moderate")
    assert opt.price_available is True
    assert opt.coverage == "complete"
    # Moderate defaults to 2nd class: 500 * 2 = 1000
    assert opt.estimated_cost_lkr == 1000.0

def test_train_calculation_partial():
    route = RouteResponse(
        trip_id="T1",
        route_summary={"start_location": "Colombo", "destinations": ["Ella"], "total_distance_km": 10, "total_estimated_duration_minutes": 10},
        legs=[
            {"from_location": "Colombo", "to_location": "Kandy", "coordinates": {}, "route_score": {"total": 1, "breakdown": {}}},
            {"from_location": "Kandy", "to_location": "Ella", "coordinates": {}, "route_score": {"total": 1, "breakdown": {}}}
        ],
        data_sources=[], limitations=[]
    )
    train_df = pd.DataFrame([{"Station": "Kandy", "2nd_Class_Rs": 500, "fare_valid": True}])
    opt = _calculate_train(route, train_df, 2, "moderate")
    assert opt.price_available is False
    assert opt.coverage == "partial"
    assert opt.estimated_cost_lkr == 1000.0 # Subtotal kept but price_available = False

def test_taxi_calculation_semantics_unverified():
    route = RouteResponse(
        trip_id="T1",
        route_summary={"start_location": "A", "destinations": ["B"], "total_distance_km": 10, "total_estimated_duration_minutes": 10},
        legs=[], data_sources=[], limitations=[]
    )
    taxi_df = pd.DataFrame([
        {"mode": "rental", "provider": "Test", "base_fare": 1000, "per_km": 10, "availability": "listed", "pricing_valid": True}
    ])
    
    options = _calculate_taxi(route, taxi_df)
    assert len(options) == 1
    assert options[0].price_available is False
    assert options[0].breakdown["raw_base_fare"] == 1000

def test_recommend_transport_and_savings():
    options = [
        TransportOption(mode="train", price_available=True, coverage="complete", estimated_cost_lkr=2000),
        TransportOption(mode="bus", price_available=True, coverage="complete", estimated_cost_lkr=1000),
        TransportOption(mode="taxi", price_available=False, coverage="unavailable", estimated_cost_lkr=0),
        TransportOption(mode="tuk", price_available=False, coverage="partial", estimated_cost_lkr=500) # Ensure partial can't win
    ]
    
    # User prefers train, train is within budget (5000)
    rec = recommend_transport(options, ["train"], 5000)
    assert rec.recommended_mode == "train"
    
    # What if budget was 1500 (train is over budget)?
    rec_low_budget = recommend_transport(options, ["train"], 1500)
    # Bus fits budget, train doesn't. Bus is 1000. 
    # Let's see: train gets -50 (budget), +30 (pref) -0.2 = -20.2
    # Bus gets +50 (budget), 0 (pref) -0.1 = +49.9
    assert rec_low_budget.recommended_mode == "bus"
    
    # Test savings opportunity: Currently selected is train (2000), budget 1500.
    savings, over_budget_amount, highest_cat, highest_pct = find_savings_opportunities(
        selected_transport=options[0], # train
        transport_options=options,
        estimated_total_cost_lkr=10000, # over a total budget of 5000
        available_budget_lkr=5000,
        acc_lkr=6000,
        food_lkr=1000,
        attr_lkr=1000
    )
    
    assert over_budget_amount == 5000.0
    assert highest_cat == "Accommodation"
    assert highest_pct == 60.0
    
    # We should have at least 2 savings: one for accommodation (generic), one for transport
    assert len(savings) >= 2
    assert any(s.category == "Transport" and s.alternative_option == "bus" for s in savings)
    assert any(s.category == "Accommodation" for s in savings)
