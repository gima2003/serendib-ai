from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

STANDARDIZED_DIR = BASE_DIR / "standardized" / "food_items"
COMBINED_DIR = BASE_DIR / "combined"

COMBINED_DIR.mkdir(exist_ok=True)

print("\n========== COMBINING FOOD ITEMS ==========\n")

files = list(STANDARDIZED_DIR.glob("*_food_items.csv"))

if not files:
    print("❌ No standardized food_items files found.")
    raise SystemExit

all_dataframes = []

for file_path in files:
    df = pd.read_csv(file_path)

    print(
        f"✅ Loaded {file_path.name} "
        f"({len(df)} rows)"
    )

    all_dataframes.append(df)

combined_df = pd.concat(
    all_dataframes,
    ignore_index=True
)

output_file = COMBINED_DIR / "food_items.csv"

combined_df.to_csv(
    output_file,
    index=False
)

print("\n============================================")
print(f"Files combined: {len(files)}")
print(f"Total rows: {len(combined_df)}")
print(f"Unique food IDs: {combined_df['food_id'].nunique()}")
print(f"Cities: {combined_df['city'].nunique()}")
print(f"Saved to: {output_file}")
print("============================================")

if len(combined_df) == combined_df["food_id"].nunique():
    print("\n✅ All food_id values remain unique.")
else:
    print("\n⚠️ Duplicate food_id values exist in the combined dataset.")