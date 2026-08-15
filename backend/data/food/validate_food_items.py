from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
STANDARDIZED_DIR = BASE_DIR / "standardized" / "food_items"

EXPECTED_COLUMNS = [
    "food_id",
    "food_name",
    "alternate_names",
    "city",
    "category",
    "meal_type",
    "typical_spice_level",
    "vegetarian_possible",
    "vegan_possible",
    "key_components",
    "description",
    "city_relevance",
    "recommendation_tags",
    "source_type",
    "source_url",
    "verified_date",
    "confidence",
]

print("\n========== FOOD ITEMS VALIDATION ==========\n")

files = list(STANDARDIZED_DIR.glob("*_food_items.csv"))

if not files:
    print("❌ No standardized food_items files found.")
    raise SystemExit

print(f"Found {len(files)} standardized food_items files.\n")

all_food_ids = []
valid_files = 0

for file_path in files:
    print("-" * 70)
    print(f"📄 {file_path.name}")

    try:
        df = pd.read_csv(file_path)

        print(f"Rows: {len(df)}")

        # 1. Schema check
        if list(df.columns) == EXPECTED_COLUMNS:
            print("✅ Schema correct")
            schema_valid = True
        else:
            print("❌ Schema mismatch")
            schema_valid = False

            missing = [
                col for col in EXPECTED_COLUMNS
                if col not in df.columns
            ]

            extra = [
                col for col in df.columns
                if col not in EXPECTED_COLUMNS
            ]

            if missing:
                print("   Missing columns:", missing)

            if extra:
                print("   Extra columns:", extra)

        # 2. food_id checks
        if "food_id" in df.columns:
            missing_ids = df["food_id"].isna().sum()
            duplicate_ids = df["food_id"].duplicated().sum()

            if missing_ids == 0:
                print("✅ No missing food_id")
            else:
                print(f"❌ Missing food_id: {missing_ids}")

            if duplicate_ids == 0:
                print("✅ No duplicate food_id inside file")
            else:
                print(f"❌ Duplicate food_id inside file: {duplicate_ids}")

            all_food_ids.extend(
                df["food_id"]
                .dropna()
                .astype(str)
                .tolist()
            )

        # 3. food_name check
        if "food_name" in df.columns:
            missing_names = df["food_name"].isna().sum()

            if missing_names == 0:
                print("✅ No missing food_name")
            else:
                print(f"❌ Missing food_name: {missing_names}")

        # 4. City check
        if "city" in df.columns:
            cities = (
                df["city"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
            )

            if len(cities) == 1:
                print(f"✅ City: {cities[0]}")
            else:
                print(f"⚠️ Multiple city values: {list(cities)}")

        # 5. Confidence range
        if "confidence" in df.columns:
            confidence = pd.to_numeric(
                df["confidence"],
                errors="coerce"
            )

            invalid_confidence = confidence[
                confidence.notna()
                & (
                    (confidence < 0)
                    | (confidence > 1)
                )
            ]

            if len(invalid_confidence) > 0:
                print(
                    f"⚠️ Confidence outside 0–1: "
                    f"{len(invalid_confidence)}"
                )

        if schema_valid:
            valid_files += 1

    except Exception as e:
        print(f"❌ Error reading file: {e}")


print("\n" + "=" * 70)
print("GLOBAL FOOD ID CHECK")
print("=" * 70)

ids = pd.Series(all_food_ids)

duplicates = ids[
    ids.duplicated(keep=False)
]

if duplicates.empty:
    print("✅ All food_id values are unique across files")
else:
    print("❌ Duplicate food_id values found across files:")
    print(
        duplicates
        .value_counts()
        .to_string()
    )


print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"Files found: {len(files)}")
print(f"Files with correct schema: {valid_files}")

if valid_files == len(files):
    print("\n✅ All standardized food_items files have the correct schema.")
else:
    print("\n⚠️ Some food_items files still need correction.")