import pandas as pd

from .text_utils import normalize_text


def rank_destinations(
    attraction_results,
    requested_interest_count
):

    if attraction_results.empty:
        return pd.DataFrame()

    rows = []

    for city, group in (
        attraction_results.groupby(
            "city"
        )
    ):

        group = group.sort_values(
            by="match_score",
            ascending=False
        )

        top_group = group.head(5)

        average_top_score = (
            top_group[
                "match_score"
            ].mean()
        )

        best_attraction_score = (
            group[
                "match_score"
            ].max()
        )

        covered_interests = set()

        for match_list in group[
            "matched_experiences"
        ]:

            for item in match_list:

                covered_interests.add(
                    normalize_text(
                        item[
                            "user_interest"
                        ]
                    )
                )

        destination_coverage = (
            len(
                covered_interests
            )
            / requested_interest_count
            if requested_interest_count
            > 0
            else 0
        )

        strong_count = len(
            group[
                group[
                    "match_score"
                ] >= 0.60
            ]
        )

        depth_score = min(
            strong_count / 5,
            1.0
        )

        final_score = (
            destination_coverage
            * 0.40
            +
            average_top_score
            * 0.30
            +
            depth_score
            * 0.20
            +
            best_attraction_score
            * 0.10
        )

        rows.append(
            {
                "city":
                    city,

                "final_score":
                    round(
                        float(
                            final_score
                        ),
                        4
                    ),

                "destination_coverage":
                    round(
                        float(
                            destination_coverage
                        ),
                        4
                    ),

                "average_top_score":
                    round(
                        float(
                            average_top_score
                        ),
                        4
                    ),

                "best_attraction_score":
                    round(
                        float(
                            best_attraction_score
                        ),
                        4
                    ),

                "matching_attractions":
                    len(group),

                "strong_attractions":
                    strong_count,
            }
        )

    results = pd.DataFrame(
        rows
    )

    return results.sort_values(
        by=[
            "final_score",
            "destination_coverage",
            "strong_attractions",
        ],
        ascending=False
    )