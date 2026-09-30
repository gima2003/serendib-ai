import profile

from models.traveller_profile import TravellerProfile  
from models.profile_readiness import profileReadiness

# checking whether is there any missing values for essential fields
def check_profile_readiness(profile: TravellerProfile) -> TravellerProfile:
    missing_context = []

    trip_basics_ready = (
        profile.duration_days is not None
        and profile.traveller_count is not None
    )

    if profile.duration_days is None:
        missing_context.append("duration_days")

    if profile.traveller_count is None:
        missing_context.append("traveller_count")


    destination_ready = (
        len(profile.interests) > 0
        or
        len(profile.preferred_destinations) > 0
        or
        len(profile.must_visit_destinations) > 0
    )

    if not destination_ready:
        missing_context.append("interests")

    food_ready = (
        len(profile.dietary_requirements) > 0
        or len(profile.food_preferences) > 0
    )

    if not food_ready:
        missing_context.append("food_preferences")


    budget_ready = (
        profile.budget is not None
    )

    planning_preferences_ready = (
        profile.crowd_preference is not None
        or
        len(profile.avoidances) > 0
        or
        len(profile.must_visit_destinations) > 0
    )


    planner_ready = (
        budget_ready
        and planning_preferences_ready
    )


    if profile.budget is None:
        missing_context.append("budget")


    if not planning_preferences_ready:
        missing_context.append("planning_preferences")


    ready = all([
        trip_basics_ready,
        destination_ready,
        food_ready,
        planner_ready,
    ])

    return profileReadiness(
        ready=ready,
        trip_basics_ready=trip_basics_ready,
        destination_ready=destination_ready,
        food_ready=food_ready,
        planner_ready=planner_ready,
        missing_context=missing_context
    )

CLARIFICATION_GROUP_PRIORITY = [
    [
        "duration_days",
        "traveller_count",
    ],
    [
        "interests",
    ],
    [
        "food_preferences",
    ],
    [
        "budget",
    ],
    [
        "planning_preferences",
    ],
]

def get_next_missing_context(
        missing_context: list[str]
) -> list[str]:

    for group in CLARIFICATION_GROUP_PRIORITY:

        pending_group = [
            context
            for context in group
            if context in missing_context
        ]

        if pending_group:
            return pending_group

    return []