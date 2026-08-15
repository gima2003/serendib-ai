from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

STANDARDIZED_DIR = BASE_DIR / "standardized" / "food_place_dishes"
COMBINED_DIR = BASE_DIR / "combined"

FOOD_PLACES_FILE = COMBINED_DIR / "food_places.csv"
FOOD_ITEMS_FILE = COMBINED_DIR / "food_items.csv"

EXPECTED_COLUMNS = [
    "link_id",
    "place_id",
    "food_id",
    "dish_match_type",
    "evidence_strength",
    "source_url",
    "notes",
]

print("\n========== FOOD PLACE DISHES VALIDATION ==========\n")

files = list(STANDARDIZED_DIR.glob("*_food_place_dishes.csv"))

if not files:
    print("❌ No standardized food_place_dishes files found.")
    raise SystemExit

print(f"Found {len(files)} standardized food_place_dishes files.\n")

# Load master IDs
food_places = pd.read_csv(FOOD_PLACES_FILE)
food_items = pd.read_csv(FOOD_ITEMS_FILE)

valid_place_ids = set(
    food_places["place_id"]
    .dropna()
    .astype(str)
)

valid_food_ids = set(
    food_items["food_id"]
    .dropna()
    .astype(str)
)

all_link_ids = []
all_rows = []
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

    # 2. Missing IDs
    for column in ["link_id", "place_id", "food_id"]:
        missing = df[column].isna().sum()

        if missing == 0:
            print(f"✅ No missing {column}")
        else:
            print(f"❌ Missing {column}: {missing}")

    # 3. Duplicate link IDs inside file
    duplicate_links = df["link_id"].duplicated().sum()

    if duplicate_links == 0:
        print("✅ No duplicate link_id inside file")
    else:
        print(f"❌ Duplicate link_id inside file: {duplicate_links}")

    # 4. Check place_id references
    invalid_places = df[
        ~df["place_id"]
        .astype(str)
        .isin(valid_place_ids)
    ]

    if invalid_places.empty:
        print("✅ All place_id references are valid")
    else:
        print(
            f"❌ Invalid place_id references: "
            f"{len(invalid_places)}"
        )

        print(
            invalid_places[
                ["link_id", "place_id", "food_id"]
            ].to_string(index=False)
        )

    # 5. Check food_id references
    invalid_foods = df[
        ~df["food_id"]
        .astype(str)
        .isin(valid_food_ids)
    ]

    if invalid_foods.empty:
        print("✅ All food_id references are valid")
    else:
        print(
            f"❌ Invalid food_id references: "
            f"{len(invalid_foods)}"
        )

        print(
            invalid_foods[
                ["link_id", "place_id", "food_id"]
            ].to_string(index=False)
        )

    all_link_ids.extend(
        df["link_id"]
        .dropna()
        .astype(str)
        .tolist()
    )

    all_rows.append(df)


# ---------------------------------------
# Global duplicate link IDs
# ---------------------------------------

print("\n" + "=" * 70)
print("GLOBAL LINK ID CHECK")
print("=" * 70)

link_series = pd.Series(all_link_ids)

duplicate_global_links = link_series[
    link_series.duplicated(keep=False)
]

if duplicate_global_links.empty:
    print("✅ All link_id values are unique across files")
else:
    print("❌ Duplicate link_id values found:")
    print(
        duplicate_global_links
        .value_counts()
        .to_string()
    )


# ---------------------------------------
# Combined relationship count
# ---------------------------------------

combined = pd.concat(
    all_rows,
    ignore_index=True
)

print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"Files found: {len(files)}")
print(f"Files with correct schema: {valid_files}")
print(f"Total relationship rows: {len(combined)}")
print(f"Unique link IDs: {combined['link_id'].nunique()}")