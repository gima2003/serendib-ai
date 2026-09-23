from datetime import date
from typing import Optional

from models.guided_planner import GuidedPlannerRequest
from models.traveller_profile import (
    TravellerProfile,
    Budget,
    Interest,
    BudgetScope,
    PreferenceStrength,
    TravelType,
    BudgetFlexibility,
    TravelPace,
    CrowdPreference,
)
from models.planning_preferences import PlanningPreferences

def calculate_duration(
    start_date: Optional[date],
    end_date: Optional[date],
) -> Optional[int]:
    """
    Calculate trip duration from the selected start and end dates.
    """

    if not start_date or not end_date:
        return None

    return (end_date - start_date).days


def normalize_travel_type(value: Optional[TravelType]):
    """
    Guided Planner already uses the same enum values,
    so no additional conversion is required here.
    """

    return value


def normalize_budget_flexibility(
    value: Optional[BudgetFlexibility],
):
    return value


def normalize_travel_pace(
    value: Optional[TravelPace],
):
    return value


def normalize_crowd_preference(
    value: Optional[CrowdPreference],
):
    return value


def build_interests(
    interests: list[str],
) -> list[Interest]:
    """
    Every interest explicitly selected in the Guided Planner
    is treated as a strong preference.
    """

    return [
        Interest(
            name=interest.strip().lower(),
            preference=PreferenceStrength.high,
        )
        for interest in interests
        if interest.strip()
    ]


def build_budget(request: GuidedPlannerRequest) -> Optional[Budget]:
    """
    Convert Guided Planner budget into the application's
    canonical Budget model.
    """

    if not request.budget:
        return None

    if request.budget.amount is None:
        return None

    return Budget(
        amount=request.budget.amount,
        currency=(
            request.budget.currency.upper()
            if request.budget.currency
            else None
        ),
        scope=BudgetScope.total_trip,
        flexibility=request.budget.flexibility,
    )


def build_dietary_requirements(
    dietary_preference: Optional[str],
) -> list[str]:
    """
    'No restriction' means there is no dietary constraint.
    """

    if not dietary_preference:
        return []

    if dietary_preference.strip().lower() == "no restriction":
        return []

    return [dietary_preference.strip().lower()]


def build_additional_requests(
    additional_notes: Optional[str],
) -> list[str]:
    if not additional_notes:
        return []

    cleaned = additional_notes.strip()

    if not cleaned:
        return []

    return [cleaned]


def build_traveller_profile(
    request: GuidedPlannerRequest,
) -> TravellerProfile:
    """
    Convert structured Guided Planner input into the
    canonical TravellerProfile used by the application.
    """

    duration_days = calculate_duration(
        request.start_date,
        request.end_date,
    )

    profile = TravellerProfile(
        duration_days=duration_days,

        traveller_count=request.traveller_count,

        travel_type=normalize_travel_type(
            request.traveller_type
        ),

        starting_location=request.origin,

        budget=build_budget(request),

        interests=build_interests(
            request.interests
        ),

        dietary_requirements=build_dietary_requirements(
            request.dietary_preference
        ),

        food_preferences=[
            food.strip().lower()
            for food in request.food_preferences
            if food.strip()
        ],

        travel_pace=normalize_travel_pace(
            request.travel_pace
        ),

        crowd_preference=normalize_crowd_preference(
            request.crowd_preference
        ),

        preferred_destinations=[
            region.strip()
            for region in request.preferred_regions
            if region.strip()
        ],

        additional_requests=build_additional_requests(
            request.additional_notes
        ),
    )

    return profile

from models.profile_state import ProfileState
from services.profile_state_service import create_profile_state

def build_guided_profile_state(
    request: GuidedPlannerRequest,
) -> ProfileState:
    """
    Convert Guided Planner input into the common
    ProfileState used by the application.
    """

    profile = build_traveller_profile(request)

    profile_state = create_profile_state(profile)

    profile_state.planning_preferences = PlanningPreferences(
        travel_style=request.travel_style,

        accommodation_preferences=[
            item.strip().lower()
            for item in request.accommodation_preferences
            if item.strip()
        ],

        transport_preferences=[
            item.strip().lower()
            for item in request.transport_preferences
            if item.strip()
        ],

        selected_activities=[
            item.strip()
            for item in request.selected_activities
            if item.strip()
        ],
    )

    return profile_state