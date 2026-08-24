from .data_loader import load_data
from .interest_matcher import (
    match_interests_to_experiences
)
from .attraction_ranker import (
    score_attractions
)
from .destination_ranker import (
    rank_destinations
)
from .text_utils import normalize_text


def recommend_destinations(
    interests,
    top_destinations=5,
    top_attractions=5,
    debug=False
):

    (
        attractions,
        experiences,
        relationships
    ) = load_data()

    matched_experiences = (
        match_interests_to_experiences(
            interests,
            experiences
        )
    )

    if not matched_experiences:

        return {
            "input_interests":
                interests,

            "matched_experiences":
                [],

            "unmatched_interests":
                interests,

            "recommended_destinations":
                [],
        }

    matched_interest_names = {
        normalize_text(
            item[
                "interest"
            ]
        )
        for item
        in matched_experiences
    }

    unmatched_interests = [
        interest
        for interest in interests
        if normalize_text(
            interest
        )
        not in matched_interest_names
    ]

    attraction_results = (
        score_attractions(
            matched_experiences,
            attractions,
            relationships
        )
    )

    # Count unique matched experience IDs.
    #
    # Example:
    # heritage -> EXP017
    # history  -> EXP017
    #
    # Both represent the same experience requirement.

    requested_experience_ids = {
        item["experience_id"]
        for item in matched_experiences
    }

    destination_results = (
        rank_destinations(
            attraction_results,
            requested_experience_count=len(
                requested_experience_ids
            )
        )
    )

    recommendations = []

    for _, destination in (
        destination_results
        .head(
            top_destinations
        )
        .iterrows()
    ):

        city = destination[
            "city"
        ]

        city_attractions = (
            attraction_results[
                attraction_results[
                    "city"
                ]
                == city
            ]
            .head(
                top_attractions
            )
        )

        attraction_list = []

        for _, attraction in (
            city_attractions.iterrows()
        ):

            item = {
                "attraction_id":
                    attraction[
                        "attraction_id"
                    ],

                "name":
                    attraction[
                        "attraction_name"
                    ],

                "category":
                    attraction[
                        "category"
                    ],

                "sub_category":
                    attraction[
                        "sub_category"
                    ],

                "match_score":
                    round(
                        float(
                            attraction[
                                "match_score"
                            ]
                        ),
                        3
                    ),

                "coverage_score":
                    round(
                        float(
                            attraction[
                                "coverage_score"
                            ]
                        ),
                        3
                    ),
            }

            if debug:

                item[
                    "debug_matches"
                ] = attraction[
                    "matched_experiences"
                ]

            attraction_list.append(
                item
            )

        recommendations.append(
            {
                "destination":
                    city,

                "score":
                    round(
                        float(
                            destination[
                                "final_score"
                            ]
                        ),
                        3
                    ),

                "interest_coverage":
                    round(
                        float(
                            destination[
                                "destination_coverage"
                            ]
                        ),
                        3
                    ),

                "matching_attractions":
                    int(
                        destination[
                            "matching_attractions"
                        ]
                    ),

                "strong_attractions":
                    int(
                        destination[
                            "strong_attractions"
                        ]
                    ),

                "attractions":
                    attraction_list,
            }
        )

    return {
        "input_interests":
            interests,

        "matched_experiences":
            matched_experiences,

        "unmatched_interests":
            unmatched_interests,

        "recommended_destinations":
            recommendations,
    }