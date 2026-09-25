from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

STANDARDIZED_DIR = (
    BASE_DIR / "standardized" / "evaluation_queries"
)

COMBINED_DIR = BASE_DIR / "combined"
FOOD_PLACES_FILE = COMBINED_DIR / "food_places.csv"

EXPECTED_COLUMNS = [
    "query_id",
    "city",
    "sample_user_query",
    "expected_filters_or_intent",
    "relevant_place_ids",
    "expected_result_text",
    "notes",
]

print("\n========== EVALUATION QUERIES VALIDATION ==========\n")

files = list(
    STANDARDIZED_DIR.glob("*_evaluation_queries.csv")
)

if not files:
    print("❌ No standardized evaluation query files found.")
    raise SystemExit

print(f"Found {len(files)} standardized files.\n")

# --------------------------------------------------
# Load valid food place IDs
# --------------------------------------------------

food_places = pd.read_csv(FOOD_PLACES_FILE)

valid_place_ids = set(
    food_places["place_id"]
    .dropna()
    .astype(str)
    .str.strip()
)

all_query_ids = []
all_rows = []
valid_files = 0
total_invalid_targets = 0

# --------------------------------------------------
# Validate each file
# --------------------------------------------------

for file_path in files:

    print("-" * 70)
    print(f"📄 {file_path.name}")

    try:
        df = pd.read_csv(file_path)

        print(f"Rows: {len(df)}")

        # ------------------------------------------
        # 1. Schema validation
        # ------------------------------------------

        if list(df.columns) == EXPECTED_COLUMNS:
            print("✅ Schema correct")
            valid_files += 1
        else:
            print("❌ Schema mismatch")

            missing_columns = [
                column
                for column in EXPECTED_COLUMNS
                if column not in df.columns
            ]

            extra_columns = [
                column
                for column in df.columns
                if column not in EXPECTED_COLUMNS
            ]

            if missing_columns:
                print(
                    f"   Missing columns: {missing_columns}"
                )

            if extra_columns:
                print(
                    f"   Extra columns: {extra_columns}"
                )

        # ------------------------------------------
        # 2. Critical field validation
        # ------------------------------------------

        critical_columns = [
            "query_id",
            "city",
            "sample_user_query",
        ]

        for column in critical_columns:

            if column not in df.columns:
                continue

            missing = df[column].isna().sum()

            blank = (
                df[column]
                .dropna()
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )

            if missing == 0 and blank == 0:
                print(f"✅ No missing {column}")
            else:

                if missing > 0:
                    print(
                        f"❌ Missing {column}: {missing}"
                    )

                if blank > 0:
                    print(
                        f"❌ Blank {column}: {blank}"
                    )

        # ------------------------------------------
        # 3. Duplicate query IDs inside file
        # ------------------------------------------

        if "query_id" in df.columns:

            duplicate_ids = (
                df["query_id"]
                .duplicated()
                .sum()
            )

            if duplicate_ids == 0:
                print(
                    "✅ No duplicate query_id inside file"
                )
            else:
                print(
                    f"❌ Duplicate query_id inside file: "
                    f"{duplicate_ids}"
                )

            all_query_ids.extend(
                df["query_id"]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )

        # ------------------------------------------
        # 4. Validate relevant targets
        # ------------------------------------------
        #
        # relevant_place_ids can contain:
        #
        #   COL-P001
        #   COL-P001,COL-P002
        #
        # OR area-level targets such as:
        #
        #   AREA:GALLE_FACE
        #
        # AREA: targets are valid evaluation targets
        # even though they are not restaurant IDs.
        # ------------------------------------------

        if "relevant_place_ids" in df.columns:

            for _, row in df.iterrows():

                value = row.get("relevant_place_ids")

                if pd.isna(value):
                    continue

                targets = [
                    item.strip()
                    for item in str(value)
                    .replace("|", ",")
                    .replace(";", ",")
                    .split(",")
                    if item.strip()
                ]

                invalid_targets = []

                for target in targets:

                    # Area-level target
                    if target.upper().startswith("AREA:"):
                        continue

                    # Valid restaurant place_id
                    if target in valid_place_ids:
                        continue

                    # Anything else is invalid
                    invalid_targets.append(target)

                if invalid_targets:

                    total_invalid_targets += len(
                        invalid_targets
                    )

                    print(
                        f"⚠️ {row['query_id']} has invalid "
                        f"evaluation targets: "
                        f"{invalid_targets}"
                    )

        all_rows.append(df)

    except Exception as e:
        print(
            f"❌ Error reading {file_path.name}: {e}"
        )


# --------------------------------------------------
# Global query ID validation
# --------------------------------------------------

print("\n" + "=" * 70)
print("GLOBAL QUERY ID CHECK")
print("=" * 70)

query_series = pd.Series(
    all_query_ids,
    dtype="object"
)

duplicate_global_ids = query_series[
    query_series.duplicated(keep=False)
]

if duplicate_global_ids.empty:

    print(
        "✅ All query_id values are globally unique"
    )

else:

    print("❌ Duplicate query_id values found:")

    print(
        duplicate_global_ids
        .value_counts()
        .to_string()
    )


# --------------------------------------------------
# Combined summary
# --------------------------------------------------

if all_rows:

    combined = pd.concat(
        all_rows,
        ignore_index=True
    )

else:

    combined = pd.DataFrame()


print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"Files found: {len(files)}")
print(
    f"Files with correct schema: "
    f"{valid_files}"
)
print(
    f"Total evaluation queries: "
    f"{len(combined)}"
)

if not combined.empty:

    print(
        f"Unique query IDs: "
        f"{combined['query_id'].nunique()}"
    )

print(
    f"Invalid evaluation targets: "
    f"{total_invalid_targets}"
)


# --------------------------------------------------
# Final result
# --------------------------------------------------

schema_ok = (
    valid_files == len(files)
)

query_ids_ok = (
    duplicate_global_ids.empty
)

targets_ok = (
    total_invalid_targets == 0
)

if (
    schema_ok
    and query_ids_ok
    and targets_ok
):

    print(
        "\n✅ Evaluation query dataset passed validation."
    )

else:

    print(
        "\n⚠️ Evaluation query dataset still has "
        "issues to review."
    )