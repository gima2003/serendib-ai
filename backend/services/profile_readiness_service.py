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


    destination_ready = len(profile.interests) > 0

    if not destination_ready:
        missing_context.append("interests")


    food_ready = (
        len(profile.dietary_requirements) > 0
        or len(profile.food_preferences) > 0
    )

    if not food_ready:
        missing_context.append("food_preferences")


    planner_ready = any([
        profile.budget is not None,
        profile.travel_pace is not None,
        profile.crowd_preference is not None,
        len(profile.avoidances) > 0,
        len(profile.must_visit_destinations) > 0,
    ])

    if not planner_ready:
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

CLARIFICATION_PRIORITY = [
    "duration_days",
    "traveller_count",
    "destination_prefrences",
    "food_preferences",
    "planning_preferences"
]

def get_next_missing_context(
        missing_context: list[str]
) -> str | None:

    for context_name in CLARIFICATION_PRIORITY:
        if context_name in missing_context:
            return context_name
    return None