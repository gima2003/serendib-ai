from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. File locations
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
COMBINED_DIR = BASE_DIR / "combined"

ATTRACTIONS_FILE = COMBINED_DIR / "attractions.csv"
EXPERIENCES_FILE = COMBINED_DIR / "experiences.csv"
RELATIONSHIPS_FILE = COMBINED_DIR / "attraction_experiences.csv"


# ---------------------------------------------------------
# 2. Main validation
# ---------------------------------------------------------

def main():

    print("\n==========================================")
    print("AGENT 2 - RELATIONSHIP VALIDATION")
    print("==========================================\n")

    # Check required files exist
    required_files = [
        ATTRACTIONS_FILE,
        EXPERIENCES_FILE,
        RELATIONSHIPS_FILE,
    ]

    for file_path in required_files:
        if not file_path.exists():
            print(f"[ERROR] Missing file: {file_path}")
            return

    # Load datasets
    attractions = pd.read_csv(ATTRACTIONS_FILE)
    experiences = pd.read_csv(EXPERIENCES_FILE)
    relationships = pd.read_csv(RELATIONSHIPS_FILE)

    errors = []

    # -----------------------------------------------------
    # 3. Check required relationship columns
    # -----------------------------------------------------

    required_columns = [
        "attraction_id",
        "experience_id",
        "relevance_score",
        "matched_activity",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in relationships.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing relationship columns: {missing_columns}"
        )

    # Stop if structure is wrong
    if missing_columns:

        print("VALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        return

    # -----------------------------------------------------
    # 4. Valid attraction IDs
    # -----------------------------------------------------

    valid_attraction_ids = set(
        attractions["attraction_id"].astype(str)
    )

    relationship_attraction_ids = set(
        relationships["attraction_id"].astype(str)
    )

    invalid_attraction_ids = (
        relationship_attraction_ids
        - valid_attraction_ids
    )

    if invalid_attraction_ids:

        errors.append(
            "Invalid attraction IDs: "
            f"{sorted(invalid_attraction_ids)}"
        )

    # -----------------------------------------------------
    # 5. Valid experience IDs
    # -----------------------------------------------------

    valid_experience_ids = set(
        experiences["experience_id"].astype(str)
    )

    relationship_experience_ids = set(
        relationships["experience_id"].astype(str)
    )

    invalid_experience_ids = (
        relationship_experience_ids
        - valid_experience_ids
    )

    if invalid_experience_ids:

        errors.append(
            "Invalid experience IDs: "
            f"{sorted(invalid_experience_ids)}"
        )

    # -----------------------------------------------------
    # 6. Duplicate relationships
    # -----------------------------------------------------

    duplicate_count = relationships.duplicated(
        subset=[
            "attraction_id",
            "experience_id",
        ]
    ).sum()

    if duplicate_count > 0:

        errors.append(
            f"{duplicate_count} duplicate "
            "attraction-experience relationship(s)"
        )

    # -----------------------------------------------------
    # 7. Attractions without experiences
    # -----------------------------------------------------

    unmapped_attractions = (
        valid_attraction_ids
        - relationship_attraction_ids
    )

    if unmapped_attractions:

        errors.append(
            "Attractions without experience mappings: "
            f"{sorted(unmapped_attractions)}"
        )

    # -----------------------------------------------------
    # 8. Validate relevance scores
    # -----------------------------------------------------

    numeric_scores = pd.to_numeric(
        relationships["relevance_score"],
        errors="coerce"
    )

    invalid_score_mask = (
        numeric_scores.isna()
        |
        ~numeric_scores.between(0, 1)
    )

    invalid_score_count = (
        invalid_score_mask.sum()
    )

    if invalid_score_count > 0:

        errors.append(
            f"{invalid_score_count} invalid "
            "relevance score(s)"
        )

    # -----------------------------------------------------
    # 9. Check missing matched activities
    # -----------------------------------------------------

    missing_activity_count = (
        relationships["matched_activity"]
        .isna()
        .sum()
    )

    if missing_activity_count > 0:

        errors.append(
            f"{missing_activity_count} relationship(s) "
            "have missing matched_activity"
        )

    # -----------------------------------------------------
    # 10. Summary
    # -----------------------------------------------------

    print(
        f"Attractions             : "
        f"{len(attractions)}"
    )

    print(
        f"Experiences             : "
        f"{len(experiences)}"
    )

    print(
        f"Relationships           : "
        f"{len(relationships)}"
    )

    print(
        f"Mapped attractions      : "
        f"{relationships['attraction_id'].nunique()}"
    )

    print(
        f"Experiences used        : "
        f"{relationships['experience_id'].nunique()}"
    )

    print(
        f"Duplicate relationships: "
        f"{duplicate_count}"
    )

    print(
        f"Unmapped attractions    : "
        f"{len(unmapped_attractions)}"
    )

    print(
        f"Invalid scores          : "
        f"{invalid_score_count}"
    )

    # -----------------------------------------------------
    # 11. Final result
    # -----------------------------------------------------

    if errors:

        print("\nVALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

    else:

        print("\nVALIDATION PASSED")

        print(
            "All attraction-experience "
            "relationships are valid."
        )


if __name__ == "__main__":
    main()