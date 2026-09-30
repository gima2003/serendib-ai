from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
COMBINED_DIR = BASE_DIR / "combined"

COMBINED_DIR.mkdir(exist_ok=True)

food_place_files = list(RAW_DIR.rglob("food_places.csv"))

print("\n========== COMBINING FOOD PLACES ==========\n")

all_dataframes = []

for file_path in food_place_files:
    df = pd.read_csv(file_path)

    print(
        f"✅ Loaded {file_path.relative_to(BASE_DIR)} "
        f"({len(df)} rows)"
    )

    all_dataframes.append(df)

combined_df = pd.concat(
    all_dataframes,
    ignore_index=True
)

output_file = COMBINED_DIR / "food_places.csv"

combined_df.to_csv(
    output_file,
    index=False
)

print("\n============================================")
print(f"Total city files combined: {len(food_place_files)}")
print(f"Total rows: {len(combined_df)}")
print(f"Saved to: {output_file}")
print("============================================")