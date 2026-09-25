from pathlib import Path
import pandas as pd

# This script is already inside backend/data/food/
FOOD_DATA_DIR = Path(__file__).resolve().parent

EXPECTED_COLUMNS = [
    "place_id",
    "place_name",
    "city",
    "area",
    "address",
    "place_type",
    "cuisine_focus",
    "local_food_strength",
    "dietary_strength",
    "price_band_lkr",
    "rating",
    "review_count",
    "opening_hours",
    "phone",
    "signature_or_recommended_dishes",
    "best_for",
    "source_type",
    "source_url",
    "verified_date",
    "confidence",
]

print("\n========== FOOD PLACES VALIDATION ==========\n")

# Find every CSV whose filename contains "food_places"
food_place_files = list(FOOD_DATA_DIR.rglob("*food_places*.csv"))

if not food_place_files:
    print("❌ No food_places CSV files found.")
    raise SystemExit

print(f"Found {len(food_place_files)} food_places files.\n")

all_place_ids = []
valid_files = 0

for file_path in food_place_files:
    print("-" * 70)
    print(f"📄 {file_path.relative_to(FOOD_DATA_DIR)}")

    try:
        df = pd.read_csv(file_path)

        print(f"Rows: {len(df)}")

        # 1. Check schema
        actual_columns = list(df.columns)

        if actual_columns == EXPECTED_COLUMNS:
            print("✅ Schema correct")
            schema_valid = True
        else:
            print("❌ Schema mismatch")
            schema_valid = False

            missing_columns = [
                col for col in EXPECTED_COLUMNS
                if col not in actual_columns
            ]

            extra_columns = [
                col for col in actual_columns
                if col not in EXPECTED_COLUMNS
            ]

            if missing_columns:
                print("   Missing columns:", missing_columns)

            if extra_columns:
                print("   Extra columns:", extra_columns)

            if (
                not missing_columns
                and not extra_columns
                and actual_columns != EXPECTED_COLUMNS
            ):
                print("   ⚠️ Columns exist but are in the wrong order")

        # 2. Check place_id
        if "place_id" in df.columns:
            missing_ids = df["place_id"].isna().sum()
            duplicate_ids = df["place_id"].duplicated().sum()

            if missing_ids == 0:
                print("✅ No missing place_id")
            else:
                print(f"❌ Missing place_id: {missing_ids}")

            if duplicate_ids == 0:
                print("✅ No duplicate place_id inside file")
            else:
                print(
                    f"❌ Duplicate place_id inside file: {duplicate_ids}"
                )

            ids = df["place_id"].dropna().astype(str).tolist()
            all_place_ids.extend(ids)

        # 3. Check city field
        if "city" in df.columns:
            city_values = df["city"].dropna().astype(str).str.strip()

            unique_cities = city_values.unique()

            if len(unique_cities) == 1:
                print(f"✅ City: {unique_cities[0]}")
            else:
                print(
                    f"⚠️ Multiple city values found: {list(unique_cities)}"
                )

            missing_city = df["city"].isna().sum()

            if missing_city > 0:
                print(f"❌ Missing city values: {missing_city}")

        # 4. Check important fields
        important_columns = [
            "place_id",
            "place_name",
            "city",
        ]

        for column in important_columns:
            if column in df.columns:
                missing_count = df[column].isna().sum()

                if missing_count > 0:
                    print(
                        f"❌ Missing values in {column}: {missing_count}"
                    )

        # 5. Check blank strings
        for column in ["place_id", "place_name", "city"]:
            if column in df.columns:
                blank_count = (
                    df[column]
                    .astype(str)
                    .str.strip()
                    .eq("")
                    .sum()
                )

                if blank_count > 0:
                    print(
                        f"❌ Blank values in {column}: {blank_count}"
                    )

        # 6. Check rating range
        if "rating" in df.columns:
            rating_numeric = pd.to_numeric(
                df["rating"],
                errors="coerce"
            )

            invalid_ratings = rating_numeric[
                rating_numeric.notna()
                & (
                    (rating_numeric < 0)
                    | (rating_numeric > 5)
                )
            ]

            if len(invalid_ratings) > 0:
                print(
                    f"⚠️ Invalid rating values: {len(invalid_ratings)}"
                )

        # 7. Check review_count
        if "review_count" in df.columns:
            review_numeric = pd.to_numeric(
                df["review_count"],
                errors="coerce"
            )

            negative_reviews = review_numeric[
                review_numeric.notna()
                & (review_numeric < 0)
            ]

            if len(negative_reviews) > 0:
                print(
                    f"⚠️ Negative review_count values: "
                    f"{len(negative_reviews)}"
                )

        # 8. Check confidence
        if "confidence" in df.columns:
            confidence_numeric = pd.to_numeric(
                df["confidence"],
                errors="coerce"
            )

            # Assumes confidence is stored from 0 to 1
            invalid_confidence = confidence_numeric[
                confidence_numeric.notna()
                & (
                    (confidence_numeric < 0)
                    | (confidence_numeric > 1)
                )
            ]

            if len(invalid_confidence) > 0:
                print(
                    f"⚠️ Confidence outside 0-1 range: "
                    f"{len(invalid_confidence)}"
                )

        if schema_valid:
            valid_files += 1

    except Exception as e:
        print(f"❌ Error reading file: {e}")


# Global duplicate ID check
print("\n" + "=" * 70)
print("GLOBAL PLACE ID CHECK")
print("=" * 70)

if all_place_ids:
    ids_series = pd.Series(all_place_ids)

    duplicate_global_ids = ids_series[
        ids_series.duplicated(keep=False)
    ]

    if duplicate_global_ids.empty:
        print("✅ All place_id values are unique across files")
    else:
        print("❌ Duplicate place_id values found across files:")
        print(
            duplicate_global_ids
            .value_counts()
            .to_string()
        )


# Final summary
print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"Files found: {len(food_place_files)}")
print(f"Files with correct schema: {valid_files}")

if valid_files == len(food_place_files):
    print("\n✅ All food_places files have the correct schema.")
else:
    print(
        "\n⚠️ Some food_places files need correction "
        "before combining."
    )