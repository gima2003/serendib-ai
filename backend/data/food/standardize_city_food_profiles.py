from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "standardized" / "city_food_profiles"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_COLUMNS = [
    "city_id",
    "city",
    "food_identity",
    "strong_categories",
    "best_use_cases",
    "notable_food_areas",
    "social_insights",
    "verified_date",
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

print("\n========== STANDARDIZING CITY FOOD PROFILES ==========\n")

found_count = 0
missing_cities = []

for city_folder, city_name in CITY_NAMES.items():

    city_dir = RAW_DIR / city_folder
    files = list(city_dir.rglob("city_food_profile.csv"))

    if not files:
        print(f"⚠️ No city_food_profile.csv found for {city_name}")
        missing_cities.append(city_name)
        continue

    found_count += 1

    file_path = files[0]

    print(f"\n📄 Processing {city_name}")

    df = pd.read_csv(file_path)

    rename_map = {
        "categories": "strong_categories",
        "areas": "notable_food_areas",
        "insights": "social_insights",
        "verified": "verified_date",
    }

    df = df.rename(columns=rename_map)

    for column in MASTER_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[MASTER_COLUMNS]

    output_file = OUTPUT_DIR / f"{city_folder}_city_food_profile.csv"

    df.to_csv(output_file, index=False)

    print(
        f"✅ Saved {output_file.name} "
        f"({len(df)} row)"
    )

print("\n============================================")
print(f"Files standardized: {found_count}")
print(f"Missing cities: {len(missing_cities)}")

if missing_cities:
    print("Missing city food profiles for:")
    for city in missing_cities:
        print(f"  - {city}")

print("============================================")