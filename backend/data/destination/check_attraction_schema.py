from pathlib import Path
import pandas as pd

# ---------------------------------------------------------
# 1. Find the raw destination data folder
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"


# ---------------------------------------------------------
# 2. Define the columns every attraction CSV must contain
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "attraction_id",
    "attraction_name",
    "city",
    "district",
    "province",
    "category",
    "description",
    "primary_activity",
    "source_id",
    "verified_date",
]


# ---------------------------------------------------------
# 3. Validation function for one CSV file
# ---------------------------------------------------------

def validate_file(file_path):
    errors = []

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return 0, [f"Could not read file: {e}"]

    # Check whether required columns exist
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing columns: {', '.join(missing_columns)}"
        )

        # Stop deeper checks because required columns are missing
        return len(df), errors

    # Check missing attraction IDs
    missing_ids = df["attraction_id"].isna().sum()

    if missing_ids > 0:
        errors.append(
            f"{missing_ids} row(s) have missing attraction_id"
        )

    # Check missing attraction names
    missing_names = df["attraction_name"].isna().sum()

    if missing_names > 0:
        errors.append(
            f"{missing_names} row(s) have missing attraction_name"
        )

    # Check duplicates inside this file
    duplicate_ids = df[
        df["attraction_id"].duplicated(keep=False)
    ]["attraction_id"].tolist()

    if duplicate_ids:
        errors.append(
            f"Duplicate attraction IDs: {duplicate_ids}"
        )

    return len(df), errors


# ---------------------------------------------------------
# 4. Validate all attraction CSV files
# ---------------------------------------------------------

def main():

    print("\n==========================================")
    print("SERENDIB AI - AGENT 2 DATA VALIDATION")
    print("==========================================\n")

    attraction_files = sorted(
        RAW_DIR.rglob("*_attractions.csv")
    )

    if not attraction_files:
        print("No attraction CSV files found.")
        print(f"Expected location: {RAW_DIR}")
        return

    total_files = 0
    total_attractions = 0
    files_with_errors = 0

    all_ids = []

    for file_path in attraction_files:

        total_files += 1

        row_count, errors = validate_file(file_path)

        total_attractions += row_count

        relative_path = file_path.relative_to(BASE_DIR)

        if errors:

            files_with_errors += 1

            print(f"[ERROR] {relative_path}")
            print(f"        Rows: {row_count}")

            for error in errors:
                print(f"        - {error}")

        else:

            print(
                f"[OK]    {relative_path} "
                f"- {row_count} attractions"
            )

            # Read IDs for cross-file duplicate checking
            df = pd.read_csv(file_path)

            all_ids.extend(
                df["attraction_id"]
                .dropna()
                .astype(str)
                .tolist()
            )

    # ---------------------------------------------------------
    # 5. Check duplicate IDs across different city files
    # ---------------------------------------------------------

    duplicate_global_ids = sorted({
        attraction_id
        for attraction_id in all_ids
        if all_ids.count(attraction_id) > 1
    })

    print("\n==========================================")
    print("VALIDATION SUMMARY")
    print("==========================================")

    print(f"Files checked      : {total_files}")
    print(f"Total attractions  : {total_attractions}")
    print(f"Files with errors  : {files_with_errors}")

    if duplicate_global_ids:

        print("\nDuplicate IDs across files:")

        for attraction_id in duplicate_global_ids:
            print(f"  - {attraction_id}")

    if files_with_errors == 0 and not duplicate_global_ids:

        print("\nVALIDATION PASSED")
        print("All attraction datasets follow the expected schema.")

    else:

        print("\nVALIDATION FAILED")
        print("Fix the issues above before standardization.")


if __name__ == "__main__":
    main()