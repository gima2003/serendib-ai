from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "combined" / "food_places.csv"

print("\n========== VALIDATING COMBINED FOOD PLACES ==========\n")

df = pd.read_csv(FILE_PATH)

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# 1. Duplicate place IDs
duplicate_ids = df[df["place_id"].duplicated(keep=False)]

if duplicate_ids.empty:
    print("✅ No duplicate place_id values")
else:
    print("❌ Duplicate place_id values found:")
    print(
        duplicate_ids[
            ["place_id", "place_name", "city"]
        ].to_string(index=False)
    )

# 2. Missing critical values
critical_columns = [
    "place_id",
    "place_name",
    "city",
]

for column in critical_columns:
    missing = df[column].isna().sum()

    if missing == 0:
        print(f"✅ No missing values in {column}")
    else:
        print(f"❌ Missing {column}: {missing}")

# 3. City counts
print("\n========== CITY COUNTS ==========\n")

city_counts = (
    df["city"]
    .value_counts()
    .sort_index()
)

print(city_counts.to_string())

print(f"\nNumber of cities: {df['city'].nunique()}")

# 4. Rating validation
rating = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

invalid_rating = df[
    rating.notna()
    & (
        (rating < 0)
        | (rating > 5)
    )
]

if invalid_rating.empty:
    print("\n✅ All numeric ratings are between 0 and 5")
else:
    print("\n❌ Invalid ratings found:")
    print(
        invalid_rating[
            ["place_id", "place_name", "city", "rating"]
        ].to_string(index=False)
    )

# 5. Review count validation
review_count = pd.to_numeric(
    df["review_count"],
    errors="coerce"
)

negative_reviews = df[
    review_count.notna()
    & (review_count < 0)
]

if negative_reviews.empty:
    print("✅ No negative review_count values")
else:
    print("❌ Negative review_count values found")

# 6. Confidence validation
confidence = pd.to_numeric(
    df["confidence"],
    errors="coerce"
)

invalid_confidence = df[
    confidence.notna()
    & (
        (confidence < 0)
        | (confidence > 1)
    )
]

if invalid_confidence.empty:
    print("✅ Confidence values are within 0–1")
else:
    print("⚠️ Confidence values outside 0–1 found")

# 7. Final summary
print("\n========== SUMMARY ==========")

print(f"Rows: {len(df)}")
print(f"Cities: {df['city'].nunique()}")
print(f"Unique place IDs: {df['place_id'].nunique()}")

if (
    len(df) == df["place_id"].nunique()
    and invalid_rating.empty
):
    print("\n✅ Combined food_places.csv looks ready for the next phase.")
else:
    print("\n⚠️ Combined dataset still has issues to fix.")