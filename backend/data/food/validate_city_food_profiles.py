from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
STANDARDIZED_DIR = (
    BASE_DIR / "standardized" / "city_food_profiles"
)

EXPECTED_COLUMNS = [
    "city_id",
    "city",
    "food_identity",
    "strong_categories",
    "best_use_cases",
    "notable_food_areas",
    "social_insights",
    "verified_date",
]

print("\n========== CITY FOOD PROFILE VALIDATION ==========\n")

files = list(
    STANDARDIZED_DIR.glob("*_city_food_profile.csv")
)

if not files:
    print("❌ No standardized city_food_profile files found.")
    raise SystemExit

print(f"Found {len(files)} standardized city food profile files.\n")

all_city_ids = []
valid_files = 0

for file_path in files:

    print("-" * 70)
    print(f"📄 {file_path.name}")

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df)}")

    # 1. Schema check
    if list(df.columns) == EXPECTED_COLUMNS:
        print("✅ Schema correct")
        valid_files += 1
    else:
        print("❌ Schema mismatch")

    # 2. Each file should contain one city profile
    if len(df) == 1:
        print("✅ Exactly one city profile row")
    else:
        print(
            f"⚠️ Expected 1 row, found {len(df)}"
        )

    # 3. Critical field checks
    for column in ["city_id", "city", "food_identity"]:

        missing = df[column].isna().sum()

        if missing == 0:
            print(f"✅ No missing {column}")
        else:
            print(
                f"⚠️ Missing {column}: {missing}"
            )

    # 4. City ID uniqueness inside file
    duplicate_ids = df["city_id"].duplicated().sum()

    if duplicate_ids == 0:
        print("✅ No duplicate city_id inside file")
    else:
        print(
            f"❌ Duplicate city_id inside file: "
            f"{duplicate_ids}"
        )

    all_city_ids.extend(
        df["city_id"]
        .dropna()
        .astype(str)
        .tolist()
    )

    # 5. Show city
    cities = (
        df["city"]
        .dropna()
        .astype(str)
        .unique()
    )

    if len(cities) == 1:
        print(f"✅ City: {cities[0]}")
    else:
        print(
            f"⚠️ Multiple city values: {list(cities)}"
        )


print("\n" + "=" * 70)
print("GLOBAL CITY ID CHECK")
print("=" * 70)

city_id_series = pd.Series(all_city_ids)

duplicates = city_id_series[
    city_id_series.duplicated(keep=False)
]

if duplicates.empty:
    print("✅ All city_id values are unique")
else:
    print("❌ Duplicate city_id values found:")
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
print(f"Unique city IDs: {city_id_series.nunique()}")

if valid_files == len(files):
    print(
        "\n✅ All standardized city_food_profile "
        "files have the correct schema."
    )
else:
    print(
        "\n⚠️ Some city_food_profile files "
        "still need correction."
    )