from difflib import get_close_matches


def validate_destination(
    destination,
    available_destinations
):

    destination_clean = destination.strip().lower()


    normalized_destinations = [
        city.lower()
        for city in available_destinations
    ]


    # 1. Exact match
    if destination_clean in normalized_destinations:

        matched_destination = next(
            city
            for city in available_destinations
            if city.lower() == destination_clean
        )

        return {
            "status": "valid",
            "destination": matched_destination,
            "suggestions": []
        }


    # 2. Similar destination (typo handling)
    suggestions = get_close_matches(
        destination_clean,
        normalized_destinations,
        n=3,
        cutoff=0.6
    )


    if suggestions:

        return {
            "status": "similar",
            "destination": None,
            "suggestions": suggestions
        }


    # 3. Completely unknown
    return {
        "status": "unknown",
        "destination": None,
        "suggestions": []
    }