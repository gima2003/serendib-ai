from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "standardized" / "social_recommendations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_COLUMNS = [
    "signal_id",
    "platform",
    "place_id",
    "place_name",
    "food_or_topic",
    "signal_polarity",
    "signal_type",
    "structured_summary",
    "local_vs_tourist_signal",
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

print("\n========== STANDARDIZING SOCIAL RECOMMENDATIONS ==========\n")

for city_folder, city_name in CITY_NAMES.items():

    city_dir = RAW_DIR / city_folder
    files = list(city_dir.rglob("social_recommendations.csv"))

    if not files:
        print(f"⚠️ No social_recommendations.csv found for {city_name}")
        continue

    file_path = files[0]

    print(f"\n📄 Processing {city_name}")

    df = pd.read_csv(file_path)

    rename_map = {
        "id": "signal_id",
        "source": "platform",
        "place": "place_name",
        "topic": "food_or_topic",
        "sentiment": "signal_polarity",
        "summary": "structured_summary",
    }

    df = df.rename(columns=rename_map)

    for column in MASTER_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[MASTER_COLUMNS]

    output_file = (
        OUTPUT_DIR
        / f"{city_folder}_social_recommendations.csv"
    )

    df.to_csv(output_file, index=False)

    print(
        f"✅ Saved {output_file.name} "
        f"({len(df)} rows)"
    )

print("\n========== FINISHED ==========")