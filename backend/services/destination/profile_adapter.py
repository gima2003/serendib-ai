from .text_utils import normalize_text


def extract_destination_preferences(
    traveller_profile
):
    """
    Convert Agent 1's TravellerProfile into the
    smaller input structure required by Agent 2.

    Agent 2 should consume structured information
    rather than reinterpret the original user query.
    """

    if not isinstance(
        traveller_profile,
        dict
    ):
        raise ValueError(
            "traveller_profile must be a dictionary"
        )

    # ---------------------------------------------
    # Interests
    # ---------------------------------------------

    interests = traveller_profile.get(
        "interests",
        []
    )

    if interests is None:
        interests = []

    if not isinstance(interests, list):
        raise ValueError(
            "traveller_profile.interests "
            "must be a list"
        )

    clean_interests = []

    seen_interests = set()

    for interest in interests:

        if not interest:
            continue

        normalized = normalize_text(
            interest
        )

        if (
            normalized
            and
            normalized not in seen_interests
        ):

            seen_interests.add(
                normalized
            )

            clean_interests.append(
                interest
            )

    # ---------------------------------------------
    # Optional preferred destinations
    # ---------------------------------------------

    preferred_destinations = (
        traveller_profile.get(
            "preferred_destinations",
            []
        )
    )

    if preferred_destinations is None:
        preferred_destinations = []

    # ---------------------------------------------
    # Optional preference object
    # ---------------------------------------------

    preferences = traveller_profile.get(
        "preferences",
        {}
    )

    if preferences is None:
        preferences = {}

    crowd_preference = preferences.get(
        "crowd_preference"
    )

    travel_pace = preferences.get(
        "travel_pace"
    )

    # ---------------------------------------------
    # Return only Agent 2 relevant information
    # ---------------------------------------------

    return {
        "interests":
            clean_interests,

        "preferred_destinations":
            preferred_destinations,

        "crowd_preference":
            crowd_preference,

        "travel_pace":
            travel_pace,

        "duration_days":
            traveller_profile.get(
                "duration_days"
            ),

        "accessibility_requirements":
            traveller_profile.get(
                "accessibility_requirements",
                []
            ),
    }