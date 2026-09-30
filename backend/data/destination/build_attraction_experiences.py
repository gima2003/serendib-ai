from pathlib import Path
import pandas as pd
import re


# ---------------------------------------------------------
# 1. Folder locations
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
COMBINED_DIR = BASE_DIR / "combined"

ATTRACTIONS_FILE = COMBINED_DIR / "attractions.csv"
EXPERIENCES_FILE = COMBINED_DIR / "experiences.csv"

OUTPUT_FILE = COMBINED_DIR / "attraction_experiences.csv"


# ---------------------------------------------------------
# 2. Experience aliases
# ---------------------------------------------------------

EXPERIENCE_ALIASES = {

    "EXP001": [
    "hiking",
    "trekking",
    "mountain hiking",
    ],

    "EXP002": [
        "photography",
        "photo",
        "photos",
    ],

    "EXP003": [
        "scenic views",
        "scenery",
        "viewpoint",
        "panoramic views",
    ],

    "EXP004": [
        "waterfall visit",
        "waterfall",
    ],

    "EXP005": [
        "tea experience",
        "tea",
        "factory tour",
        "tea estate",
    ],

    "EXP006": [
        "wildlife safari",
        "safari",
        "wildlife viewing",
        "wildlife",
        "leopard watching",
    ],

    "EXP007": [
        "bird watching",
        "birdwatching",
        "birds",
    ],

    "EXP008": [
        "whale watching",
        "marine wildlife",
    ],

    "EXP009": [
        "elephant watching",
        "elephants",
    ],

    "EXP010": [
        "surfing",
        "surf",
    ],

    "EXP011": [
        "swimming",
    ],

    "EXP012": [
        "snorkeling",
        "snorkelling",
    ],

    "EXP013": [
        "diving",
        "scuba",
    ],

    "EXP014": [
        "beach relaxation",
        "beach walk",
        "beach",
    ],

    "EXP015": [
        "sunrise viewing",
        "sunrise",
    ],

    "EXP016": [
        "sunset viewing",
        "sunset",
    ],

    "EXP017": [
        "heritage exploration",
        "heritage",
        "history",
        "archaeology",
        "maritime history",
        "railway heritage",
    ],

    "EXP018": [
        "religious & spiritual visit",
        "religious visit",
        "religious",
        "spiritual",
    ],

    "EXP019": [
        "architecture exploration",
        "architecture",
    ],

    "EXP020": [
        "museum visit",
        "museum",
    ],

    "EXP021": [
        "local culture experience",
        "local culture",
        "culture",
        "urban experience",
    ],

    "EXP022": [
        "local market & shopping",
        "shopping",
        "market",
    ],

    "EXP023": [
        "cycling",
        "bike",
        "bicycle",
    ],

    "EXP024": [
        "train journey experience",
        "railway experience",
        "train journey",
        "rail journey",
    ],

    "EXP025": [
        "boating",
        "boat journey",
        "boat",
        "lagoon",
    ],

    "EXP026": [
        "adventure",
        "cave exploration",
    ],

    "EXP027": [
        "nature walk",
        "walking",
        "nature",
    ],

    "EXP028": [
        "garden & botanical visit",
        "garden visit",
        "botanical",
    ],

    "EXP029": [
        "local food",
        "food",
        "culinary",
    ],

    "EXP030": [
        "relaxation",
        "wellness",
    ],

    "EXP031": [
        "art",
    ],

    "EXP032": [
        "family experience",
    ],

    "EXP033": [
        "farm experience",
    ],
}


# ---------------------------------------------------------
# 3. Normalize text
# ---------------------------------------------------------

def normalize_text(value):

    if pd.isna(value):
        return ""

    value = str(value).lower().strip()

    # Make "&" comparable with the word "and"
    value = value.replace("&", " and ")

    # Remove punctuation
    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    # Remove repeated spaces
    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


# ---------------------------------------------------------
# 4. Split primary activities
# ---------------------------------------------------------

def split_activities(value):

    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split("|")
        if item.strip()
    ]


# ---------------------------------------------------------
# 5. Match activity to experience
# ---------------------------------------------------------

def activity_matches_experience(
    activity,
    experience_id,
    experience_name,
    preference_keywords
):

    activity_normalized = normalize_text(activity)

    possible_terms = []

    # Official experience name
    possible_terms.append(
        experience_name
    )

    # Keywords from experiences.csv
    if not pd.isna(preference_keywords):

        keywords = str(
            preference_keywords
        ).split("|")

        possible_terms.extend(
            keywords
        )

    # Extra aliases defined above
    possible_terms.extend(
        EXPERIENCE_ALIASES.get(
            experience_id,
            []
        )
    )

    for term in possible_terms:

        normalized_term = normalize_text(
            term
        )

        if not normalized_term:
            continue

        if activity_normalized == normalized_term:
            return True, 1.0

    return False, 0.0


# ---------------------------------------------------------
# 6. Build relationships
# ---------------------------------------------------------

def build_relationships(
    attractions_df,
    experiences_df
):

    relationships = []

    unmatched_activities = set()

    for _, attraction in attractions_df.iterrows():

        attraction_id = attraction[
            "attraction_id"
        ]

        activities = split_activities(
            attraction[
                "primary_activity"
            ]
        )

        # Prevent duplicate attraction → experience rows
        matched_experience_ids = set()

        for activity in activities:

            activity_was_matched = False

            for _, experience in experiences_df.iterrows():

                experience_id = experience[
                    "experience_id"
                ]

                # IMPORTANT:
                # We still check whether this activity matches
                # even if this experience was already linked.
                #
                # This fixes the false "unmatched activity" problem.
                matched, score = (
                    activity_matches_experience(
                        activity=activity,
                        experience_id=experience_id,
                        experience_name=experience[
                            "experience_name"
                        ],
                        preference_keywords=experience[
                            "preference_keywords"
                        ],
                    )
                )

                if matched:

                    # The activity itself has a valid mapping
                    activity_was_matched = True

                    # Only create a new row if this
                    # attraction-experience relationship
                    # has not already been added.
                    if (
                        experience_id
                        not in matched_experience_ids
                    ):

                        relationships.append(
                            {
                                "attraction_id":
                                    attraction_id,

                                "experience_id":
                                    experience_id,

                                "relevance_score":
                                    score,

                                "matched_activity":
                                    activity,
                            }
                        )

                        matched_experience_ids.add(
                            experience_id
                        )

            # Only truly unmatched activities reach here
            if not activity_was_matched:

                unmatched_activities.add(
                    activity
                )

    relationships_df = pd.DataFrame(
        relationships
    )

    return (
        relationships_df,
        unmatched_activities
    )


# ---------------------------------------------------------
# 7. Validate relationships
# ---------------------------------------------------------

def validate_relationships(
    relationships_df,
    attractions_df,
    experiences_df
):

    valid_attraction_ids = set(
        attractions_df[
            "attraction_id"
        ]
    )

    valid_experience_ids = set(
        experiences_df[
            "experience_id"
        ]
    )

    invalid_attractions = (
        set(
            relationships_df[
                "attraction_id"
            ]
        )
        -
        valid_attraction_ids
    )

    invalid_experiences = (
        set(
            relationships_df[
                "experience_id"
            ]
        )
        -
        valid_experience_ids
    )

    if invalid_attractions:

        raise ValueError(
            f"Invalid attraction IDs found: "
            f"{invalid_attractions}"
        )

    if invalid_experiences:

        raise ValueError(
            f"Invalid experience IDs found: "
            f"{invalid_experiences}"
        )

    duplicate_count = (
        relationships_df
        .duplicated(
            subset=[
                "attraction_id",
                "experience_id"
            ]
        )
        .sum()
    )

    if duplicate_count > 0:

        raise ValueError(
            f"{duplicate_count} duplicate "
            "attraction-experience relationships found."
        )


# ---------------------------------------------------------
# 8. Main program
# ---------------------------------------------------------

def main():

    print("\n==========================================")
    print(
        "SERENDIB AI - BUILD "
        "ATTRACTION EXPERIENCES"
    )
    print("==========================================\n")

    # -----------------------------------------------------
    # Check required input files
    # -----------------------------------------------------

    if not ATTRACTIONS_FILE.exists():

        print(
            "[ERROR] attractions.csv not found:"
        )

        print(
            ATTRACTIONS_FILE
        )

        return

    if not EXPERIENCES_FILE.exists():

        print(
            "[ERROR] experiences.csv not found:"
        )

        print(
            EXPERIENCES_FILE
        )

        print(
            "\nPlace experiences.csv inside "
            "data/destination/combined/"
        )

        return

    # -----------------------------------------------------
    # Load datasets
    # -----------------------------------------------------

    attractions_df = pd.read_csv(
        ATTRACTIONS_FILE
    )

    experiences_df = pd.read_csv(
        EXPERIENCES_FILE
    )

    print(
        f"Attractions loaded : "
        f"{len(attractions_df)}"
    )

    print(
        f"Experiences loaded : "
        f"{len(experiences_df)}"
    )

    # -----------------------------------------------------
    # Build mappings
    # -----------------------------------------------------

    relationships_df, unmatched_activities = (
        build_relationships(
            attractions_df,
            experiences_df
        )
    )

    if relationships_df.empty:

        print(
            "\n[ERROR] No experience mappings "
            "were generated."
        )

        return

    # -----------------------------------------------------
    # Validate mappings
    # -----------------------------------------------------

    validate_relationships(
        relationships_df,
        attractions_df,
        experiences_df
    )

    # -----------------------------------------------------
    # Sort result
    # -----------------------------------------------------

    relationships_df = (
        relationships_df
        .sort_values(
            by=[
                "attraction_id",
                "experience_id"
            ]
        )
        .reset_index(
            drop=True
        )
    )

    # -----------------------------------------------------
    # Save final relationship dataset
    # -----------------------------------------------------

    relationships_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------------------------------
    # Calculate summary
    # -----------------------------------------------------

    attractions_mapped = (
        relationships_df[
            "attraction_id"
        ]
        .nunique()
    )

    experiences_used = (
        relationships_df[
            "experience_id"
        ]
        .nunique()
    )

    total_attractions = len(
        attractions_df
    )

    unmapped_attractions = (
        total_attractions
        -
        attractions_mapped
    )

    # -----------------------------------------------------
    # Display summary
    # -----------------------------------------------------

    print("\n==========================================")
    print("RELATIONSHIP BUILD SUMMARY")
    print("==========================================")

    print(
        f"Relationships created : "
        f"{len(relationships_df)}"
    )

    print(
        f"Attractions mapped    : "
        f"{attractions_mapped}"
    )

    print(
        f"Unmapped attractions  : "
        f"{unmapped_attractions}"
    )

    print(
        f"Experiences used      : "
        f"{experiences_used}"
    )

    print(
        f"\nSaved to:\n"
        f"{OUTPUT_FILE}"
    )

    # -----------------------------------------------------
    # Display genuinely unmatched activities
    # -----------------------------------------------------

    if unmatched_activities:

        print(
            "\n------------------------------------------"
        )
        print("UNMATCHED ACTIVITIES")
        print("------------------------------------------")

        print(
            "These activities need manual review:"
        )

        for activity in sorted(
            unmatched_activities
        ):
            print(
                f"- {activity}"
            )

    else:

        print(
            "\nAll primary activities were matched."
        )


if __name__ == "__main__":
    main()