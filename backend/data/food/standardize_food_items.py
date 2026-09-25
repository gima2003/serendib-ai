from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "standardized" / "food_items"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_COLUMNS = [
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

print("\n========== STANDARDIZING FOOD ITEMS ==========\n")

for city_folder, city_name in CITY_NAMES.items():

    city_dir = RAW_DIR / city_folder
    files = list(city_dir.rglob("food_items.csv"))

    if not files:
        print(f"❌ No food_items.csv found for {city_name}")
        continue

    file_path = files[0]

    print(f"📄 Processing {city_name}")

    df = pd.read_csv(file_path)

    # -----------------------------------------
    # Normalize column names
    # -----------------------------------------

    rename_map = {
        "meal": "meal_type",
        "spice": "typical_spice_level",
        "spice_level": "typical_spice_level",
        f"{city_folder}_relevance": "city_relevance",
    }

    df = df.rename(columns=rename_map)

    # -----------------------------------------
    # Add city
    # -----------------------------------------

    df["city"] = city_name

    # -----------------------------------------
    # Add missing master columns
    # -----------------------------------------

    for column in MASTER_COLUMNS:
        if column not in df.columns:
            df[column] = None

    # -----------------------------------------
    # Reorder columns
    # -----------------------------------------

    df = df[MASTER_COLUMNS]

    # -----------------------------------------
    # Save standardized file
    # -----------------------------------------

    output_file = OUTPUT_DIR / f"{city_folder}_food_items.csv"

    df.to_csv(output_file, index=False)

    print(
        f"✅ Saved {output_file.name} "
        f"({len(df)} rows)"
    )

print("\n========== FINISHED ==========")