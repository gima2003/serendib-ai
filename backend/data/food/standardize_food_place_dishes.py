from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "standardized" / "food_place_dishes"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_COLUMNS = [
    "link_id",
    "place_id",
    "food_id",
    "dish_match_type",
    "evidence_strength",
    "source_url",
    "notes",
]

CITY_NAMES = {
    "arugam_bay": "Arugam Bay",
    "bandarawela": "Bandarawela",
    "colombo": "Colombo",
    "dambulla": "Dambulla",
    "ella": "Ella",
    "galle": "Galle",
    "jaffna": "Jaffna",
    "kandy": "Kandy",
    "mirissa": "Mirissa",
    "nuwara_eliya": "Nuwara Eliya",
    "sigiriya": "Sigiriya",
    "yala": "Yala",
}

print("\n========== STANDARDIZING FOOD PLACE DISHES ==========\n")

found_count = 0
missing_cities = []

for city_folder, city_name in CITY_NAMES.items():

    city_dir = RAW_DIR / city_folder
    files = list(city_dir.rglob("food_place_dishes.csv"))

    if not files:
        print(f"⚠️ No food_place_dishes.csv found for {city_name}")
        missing_cities.append(city_name)
        continue

    found_count += 1

    file_path = files[0]

    print(f"\n📄 Processing {city_name}")

    df = pd.read_csv(file_path)

    # Normalize relationship column
    if "relationship" in df.columns:
        df = df.rename(
            columns={"relationship": "dish_match_type"}
        )

        print("✅ Renamed relationship → dish_match_type")

    # Add missing columns without inventing data
    for column in MASTER_COLUMNS:
        if column not in df.columns:
            df[column] = None

    # Keep only master columns and correct order
    df = df[MASTER_COLUMNS]

    output_file = (
        OUTPUT_DIR
        / f"{city_folder}_food_place_dishes.csv"
    )

    df.to_csv(output_file, index=False)

    print(
        f"✅ Saved {output_file.name} "
        f"({len(df)} rows)"
    )

print("\n============================================")
print(f"Files standardized: {found_count}")
print(f"Missing cities: {len(missing_cities)}")

if missing_cities:
    print("Missing food_place_dishes data for:")
    for city in missing_cities:
        print(f"  - {city}")

print("============================================")