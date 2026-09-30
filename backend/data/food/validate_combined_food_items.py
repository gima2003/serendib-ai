from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "combined" / "food_items.csv"

print("\n========== VALIDATING COMBINED FOOD ITEMS ==========\n")

df = pd.read_csv(FILE_PATH)

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# 1. Duplicate IDs
duplicates = df[df["food_id"].duplicated(keep=False)]

if duplicates.empty:
    print("✅ No duplicate food_id values")
else:
    print("❌ Duplicate food_id values found")
    print(
        duplicates[
            ["food_id", "food_name", "city"]
        ].to_string(index=False)
    )

# 2. Missing critical fields
critical_columns = [
    "food_id",
    "food_name",
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

# 4. Confidence validation
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
    print("\n✅ Confidence values are within 0–1")
else:
    print("\n⚠️ Confidence values outside 0–1 found")

# 5. Final summary
print("\n========== SUMMARY ==========")

print(f"Rows: {len(df)}")
print(f"Cities: {df['city'].nunique()}")
print(f"Unique food IDs: {df['food_id'].nunique()}")

if (
    len(df) == df["food_id"].nunique()
    and df["food_id"].isna().sum() == 0
    and df["food_name"].isna().sum() == 0
    and df["city"].isna().sum() == 0
):
    print("\n✅ Combined food_items.csv looks ready for MongoDB.")
else:
    print("\n⚠️ Combined dataset still has issues to fix.")