import pytest
from backend.agents.planner.context.crowd_prediction_service import calculate_crowd_prediction

def test_weekend_crowd_increase():
    # 2026-09-19 is a Saturday, not a holiday
    prediction = calculate_crowd_prediction("2026-09-19", "Unknown Place")
    assert "Weekend" in prediction.reasons
    assert prediction.crowd_score == 20

def test_holiday_crowd_increase():
    # 2026-02-04 is a Wednesday, Public Holiday (National Day)
    prediction = calculate_crowd_prediction("2026-02-04", "Unknown Place")
    assert "National Day" in prediction.reasons
    assert prediction.crowd_score == 40
    
def test_poya_day_crowd_increase():
    # 2026-09-26 is a Saturday, Full Moon Poya Day
    prediction = calculate_crowd_prediction("2026-09-26", "Unknown Place")
    assert "Full Moon Poya Day" in prediction.reasons
    assert "Weekend" in prediction.reasons
    assert prediction.crowd_score == 30 + 20 # Poya (30) + Weekend (20) = 50

def test_popular_destination_impact():
    # 2026-09-24 is a Thursday, no holiday
    prediction = calculate_crowd_prediction("2026-09-24", "Ella")
    assert "Popular tourist area" in prediction.reasons
    assert prediction.crowd_score == 20

def test_multiple_destinations_affected_by_same_holiday():
    # 2026-09-26 is Poya + Weekend
    p1 = calculate_crowd_prediction("2026-09-26", "Ella")
    p2 = calculate_crowd_prediction("2026-09-26", "Nuwara Eliya")
    
    assert "Full Moon Poya Day" in p1.reasons
    assert "Full Moon Poya Day" in p2.reasons
    assert p1.crowd_score == p2.crowd_score
    
def test_special_poya_rule_for_religious_places():
    # 2026-09-26 is Poya + Weekend
    prediction = calculate_crowd_prediction("2026-09-26", "Kandy Temple of Tooth", category="religious")
    assert "Religious place on Poya day" in prediction.reasons
    assert "Full Moon Poya Day" in prediction.reasons
    assert "Weekend" in prediction.reasons
    assert "Popular tourist area" in prediction.reasons
    # Poya (30) + Weekend (20) + Popular (20) + Religious Poya (20) = 90
    assert prediction.crowd_score == 90
    assert prediction.crowd_level == "VERY_HIGH"

def test_long_weekend_crowd_increase():
    # 2026-05-01 is May Day (Friday). Therefore Fri, Sat, Sun are long weekend.
    prediction_fri = calculate_crowd_prediction("2026-05-01", "Unknown Place")
    assert "May Day" in prediction_fri.reasons
    assert "Long weekend" in prediction_fri.reasons
    assert prediction_fri.crowd_score == 40 + 30 # 70
    
    # 2026-05-02 is Saturday
    prediction_sat = calculate_crowd_prediction("2026-05-02", "Unknown Place")
    assert "Weekend" in prediction_sat.reasons
    assert "Long weekend" in prediction_sat.reasons
    assert prediction_sat.crowd_score == 20 + 30 # 50
