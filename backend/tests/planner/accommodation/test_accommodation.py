import pytest
from unittest.mock import patch, MagicMock

from agents.accommodation.schemas import AccommodationRequest, BudgetRequest, StayRequest, AccommodationCandidate
from agents.accommodation.accommodation_service import process_accommodation_request
from agents.accommodation.accommodation_price_service import estimate_accommodation_price
from agents.accommodation.accommodation_ranker import rank_accommodations

@patch("agents.accommodation.accommodation_service.fetch_accommodations_geoapify")
@patch("agents.accommodation.accommodation_service.enrich_accommodations_google_places")
def test_accommodation_workflow_success(mock_google, mock_geoapify):
    mock_geoapify.return_value = [
        AccommodationCandidate(
            accommodation_id="1", name="Hotel A", city="Kandy", source="Geoapify", accommodation_type="hotel"
        ),
        AccommodationCandidate(
            accommodation_id="2", name="Villa B", city="Kandy", source="Geoapify", accommodation_type="villa"
        ),
        AccommodationCandidate( # duplicate
            accommodation_id="3", name="Hotel A", city="Kandy", source="Geoapify", accommodation_type="hotel"
        )
    ]
    # Pass through
    mock_google.side_effect = lambda x: x
    
    req = AccommodationRequest(
        traveller_count=2,
        travel_type="couple",
        budget=BudgetRequest(amount=1000, currency="USD"),
        stays=[StayRequest(city="Kandy", nights=2)]
    )
    
    resp = process_accommodation_request(req)
    
    assert resp.status == "success"
    assert len(resp.accommodation_plan) == 1
    plan = resp.accommodation_plan[0]
    
    assert plan.city == "Kandy"
    assert plan.nights == 2
    
    # Deduplication should reduce 3 down to 2
    assert len(plan.hotel_options) == 2
    
    # Check selection
    assert sum(1 for h in plan.hotel_options if h.is_selected) == 1
    
    # Check prices
    for h in plan.hotel_options:
        assert h.price_information.type == "estimated_range"
        assert h.price_information.estimated_price_per_night_lkr > 0

@patch("agents.accommodation.accommodation_service.fetch_accommodations_geoapify")
@patch("agents.accommodation.accommodation_service.fetch_accommodations_osm")
def test_geoapify_fallback_osm(mock_osm, mock_geoapify):
    # Geoapify fails
    mock_geoapify.return_value = []
    
    # OSM succeeds
    mock_osm.return_value = [
        AccommodationCandidate(
            accommodation_id="OSM1", name="OSM Hotel", city="Kandy", source="OSM", accommodation_type="hotel"
        )
    ]
    
    req = AccommodationRequest(
        budget=BudgetRequest(amount=50000, currency="LKR"),
        stays=[StayRequest(city="Kandy", nights=1)]
    )
    
    resp = process_accommodation_request(req)
    assert len(resp.accommodation_plan[0].hotel_options) == 1
    assert resp.accommodation_plan[0].hotel_options[0].name == "OSM Hotel"
    assert resp.accommodation_plan[0].hotel_options[0].source == "OSM"

def test_price_estimation():
    candidate = AccommodationCandidate(
        accommodation_id="1", name="Test Resort", city="Kandy", source="Test", accommodation_type="resort"
    )
    priced = estimate_accommodation_price(candidate, 20000.0)
    assert priced.price_information.estimated_price_per_night_lkr == 27500.0 # Midpoint of 20000 and 35000
    
    candidate2 = AccommodationCandidate(
        accommodation_id="2", name="Test Hostel", city="Kandy", source="Test", accommodation_type="hostel"
    )
    priced2 = estimate_accommodation_price(candidate2, 5000.0)
    assert priced2.price_information.estimated_price_per_night_lkr == 7500.0

def test_ranking():
    candidates = [
        AccommodationCandidate(accommodation_id="1", name="A", city="K", source="test", accommodation_type="hostel"),
        AccommodationCandidate(accommodation_id="2", name="B", city="K", source="test", accommodation_type="resort")
    ]
    # Price them
    c1 = estimate_accommodation_price(candidates[0], 10000)
    c2 = estimate_accommodation_price(candidates[1], 10000)
    
    # Couple should prefer resort
    ranked = rank_accommodations([c1, c2], travel_type="couple", travel_pace="relaxed", interests=[], daily_budget_estimate=30000)
    
    assert ranked[0].name == "B"
    assert "Suitable for couple travellers" in ranked[0].recommendation_reasons
    
    # Solo should prefer hostel
    ranked2 = rank_accommodations([c1, c2], travel_type="solo", travel_pace="relaxed", interests=[], daily_budget_estimate=10000)
    assert ranked2[0].name == "A"
    assert "Great for solo travellers" in ranked2[0].recommendation_reasons
