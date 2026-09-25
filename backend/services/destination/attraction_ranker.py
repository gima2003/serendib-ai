import pandas as pd


def score_attractions(
    matched_experiences,
    attractions,
    relationships
):

    if not matched_experiences:
        return pd.DataFrame()

    experience_info = {
        item[
            "experience_id"
        ]: item
        for item in matched_experiences
    }

    requested_ids = set(
        experience_info.keys()
    )

    matched_relationships = (
        relationships[
            relationships[
                "experience_id"
            ].isin(
                requested_ids
            )
        ].copy()
    )

    if matched_relationships.empty:
        return pd.DataFrame()

    matched_relationships[
        "interest_strength"
    ] = matched_relationships[
        "experience_id"
    ].map(
        lambda experience_id:
            experience_info[
                experience_id
            ][
                "match_strength"
            ]
    )

    matched_relationships[
        "weighted_score"
    ] = (
        matched_relationships[
            "relevance_score"
        ]
        *
        matched_relationships[
            "interest_strength"
        ]
    )

    result_rows = []

    for (
        attraction_id,
        group
    ) in matched_relationships.groupby(
        "attraction_id"
    ):

        matched_ids = set(
            group[
                "experience_id"
            ]
        )

        matched_count = len(
            matched_ids
        )

        requested_count = len(
            requested_ids
        )

        coverage_score = (
            matched_count
            / requested_count
            if requested_count > 0
            else 0
        )

        relevance_score = (
            group[
                "weighted_score"
            ].mean()
        )

        full_coverage_bonus = (
            0.10
            if coverage_score == 1.0
            else 0.0
        )

        match_score = (
            coverage_score * 0.60
            +
            relevance_score * 0.40
            +
            full_coverage_bonus
        )

        match_score = min(
            match_score,
            1.0
        )

        matched_details = []

        for _, row in group.iterrows():

            experience_id = (
                row[
                    "experience_id"
                ]
            )

            info = (
                experience_info[
                    experience_id
                ]
            )

            matched_details.append(
                {
                    "user_interest":
                        info[
                            "interest"
                        ],

                    "experience_id":
                        experience_id,

                    "experience_name":
                        info[
                            "experience_name"
                        ],

                    "relationship_score":
                        float(
                            row[
                                "relevance_score"
                            ]
                        ),

                    "matched_activity":
                        row[
                            "matched_activity"
                        ],
                }
            )

        result_rows.append(
            {
                "attraction_id":
                    attraction_id,

                "match_score":
                    round(
                        float(
                            match_score
                        ),
                        4
                    ),

                "coverage_score":
                    round(
                        float(
                            coverage_score
                        ),
                        4
                    ),

                "relevance_score":
                    round(
                        float(
                            relevance_score
                        ),
                        4
                    ),

                "matched_experience_count":
                    matched_count,

                "matched_experiences":
                    matched_details,
            }
        )

    scores = pd.DataFrame(
        result_rows
    )

    results = scores.merge(
        attractions,
        on="attraction_id",
        how="left"
    )

    return results.sort_values(
        by=[
            "match_score",
            "coverage_score",
            "relevance_score",
        ],
        ascending=False
    )