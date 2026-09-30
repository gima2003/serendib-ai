from .text_utils import normalize_text


def extract_destination_preferences(
    traveller_profile
):
    """
    Convert Agent 1 TravellerProfile into
    the input structure required by Agent 2.

    Agent 2 receives structured preferences,
    not the original user conversation.
    """

    if not isinstance(
        traveller_profile,
        dict
    ):
        raise ValueError(
            "traveller_profile must be a dictionary"
        )


    # -------------------------------------------------
    # Support both formats:
    #
    # 1. Full Agent 1 state:
    # {
    #   "status":"ready",
    #   "profile": {...}
    # }
    #
    # 2. Direct profile:
    # {
    #   "duration_days":6,
    #   ...
    # }
    # -------------------------------------------------

    profile = traveller_profile.get(
        "profile",
        traveller_profile
    )


    # -------------------------------------------------
    # Interests
    # -------------------------------------------------

    interests = profile.get(
        "interests",
        []
    )


    if interests is None:
        interests = []


    if not isinstance(
        interests,
        list
    ):
        raise ValueError(
            "traveller_profile.interests must be a list"
        )


    clean_interests = []

    seen_interests = set()


    for interest in interests:


        if not interest:
            continue


        # Agent 1 format:
        #
        # {
        #    "name": "beach",
        #    "preference": "high"
        # }
        #

        if isinstance(
            interest,
            dict
        ):

            interest_name = interest.get(
                "name"
            )

        else:

            # Backward compatibility
            # if Agent 2 receives:
            # ["beach","nature"]

            interest_name = interest



        if not interest_name:
            continue



        normalized = normalize_text(
            interest_name
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
                interest_name
            )


    # -------------------------------------------------
    # Preferred destinations
    # -------------------------------------------------

    preferred_destinations = (
        profile.get(
            "preferred_destinations",
            []
        )
    )


    if preferred_destinations is None:
        preferred_destinations = []



    # -------------------------------------------------
    # Travel preferences
    #
    # Agent 1 currently sends:
    #
    # "crowd_preference": "avoid",
    # "travel_pace": "relaxed"
    #
    # directly inside profile.
    #
    # Future support:
    #
    # "preferences": {
    #      "crowd_preference":"low"
    # }
    #
    # -------------------------------------------------

    preferences = profile.get(
        "preferences",
        {}
    )


    if not preferences:

        preferences = profile



    if preferences is None:

        preferences = {}



    crowd_preference = preferences.get(
        "crowd_preference"
    )


    travel_pace = preferences.get(
        "travel_pace"
    )


    # -------------------------------------------------
    # Return Agent 2 input
    # -------------------------------------------------

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
            profile.get(
                "duration_days"
            ),


        "accessibility_requirements":
            profile.get(
                "accessibility_requirements",
                []
            ),

    }