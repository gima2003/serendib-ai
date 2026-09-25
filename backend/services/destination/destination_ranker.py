import pandas as pd


def rank_destinations(
    attraction_results,
    requested_experience_count
):

    if attraction_results.empty:
        return pd.DataFrame()

    rows = []

    for city, group in attraction_results.groupby("city"):

        group = group.sort_values(
            by="match_score",
            ascending=False
        )

        # Use the best five matching attractions
        # when measuring overall destination quality.
        top_group = group.head(5)

        average_top_score = (
            top_group["match_score"].mean()
        )

        best_attraction_score = (
            group["match_score"].max()
        )

        # -------------------------------------------------
        # EXPERIENCE COVERAGE
        # -------------------------------------------------
        #
        # We use unique experience IDs instead of the
        # original user words.
        #
        # Example:
        # heritage -> EXP017
        # history  -> EXP017
        #
        # These count as ONE experience, not two.
        # -------------------------------------------------

        covered_experience_ids = set()

        for match_list in group["matched_experiences"]:

            for item in match_list:

                covered_experience_ids.add(
                    item["experience_id"]
                )

        if requested_experience_count > 0:

            destination_coverage = (
                len(covered_experience_ids)
                / requested_experience_count
            )

        else:
            destination_coverage = 0

        destination_coverage = min(
            destination_coverage,
            1.0
        )

        # -------------------------------------------------
        # STRONG ATTRACTIONS
        # -------------------------------------------------
        #
        # Previously we used >= 0.60.
        #
        # But 0.60 can represent only ONE generic interest
        # such as Photography.
        #
        # >= 0.75 requires a stronger overall match.
        # -------------------------------------------------

        strong_attractions = group[
            group["match_score"] >= 0.75
        ]

        strong_count = len(
            strong_attractions
        )

        # Five strong attractions gives
        # the full depth score.
        depth_score = min(
            strong_count / 5,
            1.0
        )

        # -------------------------------------------------
        # FINAL DESTINATION SCORE
        # -------------------------------------------------

        final_score = (
            destination_coverage * 0.40
            +
            average_top_score * 0.30
            +
            depth_score * 0.20
            +
            best_attraction_score * 0.10
        )

        final_score = min(
            final_score,
            1.0
        )

        rows.append(
            {
                "city": city,

                "final_score": round(
                    float(final_score),
                    4
                ),

                "destination_coverage": round(
                    float(destination_coverage),
                    4
                ),

                "average_top_score": round(
                    float(average_top_score),
                    4
                ),

                "best_attraction_score": round(
                    float(best_attraction_score),
                    4
                ),

                "matching_attractions": len(group),

                "strong_attractions": strong_count,
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