from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "standardized" / "food_place_dishes"

CITY_PREFIXES = {
    "arugam_bay": "ABY",
    "bandarawela": "BDR",
    "colombo": "COL",
    "dambulla": "DAM",
    "ella": "ELL",
    "mirissa": "MIR",
    "sigiriya": "SIG",
    "yala": "YAL",
}

print("\n========== FIXING FOOD PLACE DISH LINK IDS ==========\n")

files = list(DATA_DIR.glob("*_food_place_dishes.csv"))

for file_path in files:
    filename = file_path.name

    city_key = None

    for key in CITY_PREFIXES:
        if filename.startswith(key):
            city_key = key
            break

    if not city_key:
        print(f"⚠️ Could not identify city for {filename}")
        continue

    prefix = CITY_PREFIXES[city_key]

    df = pd.read_csv(file_path)

    df["link_id"] = df["link_id"].astype(str).apply(
        lambda x: f"{prefix}-{x}"
        if not x.startswith(f"{prefix}-")
        else x
    )

    df.to_csv(file_path, index=False)

    print(
        f"✅ Updated {filename} "
        f"with prefix {prefix}"
    )

print("\n========== FINISHED ==========")