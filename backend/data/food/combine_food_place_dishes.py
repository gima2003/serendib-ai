from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

STANDARDIZED_DIR = (
    BASE_DIR / "standardized" / "food_place_dishes"
)

COMBINED_DIR = BASE_DIR / "combined"

COMBINED_DIR.mkdir(exist_ok=True)

print("\n========== COMBINING FOOD PLACE DISHES ==========\n")

files = list(
    STANDARDIZED_DIR.glob("*_food_place_dishes.csv")
)

if not files:
    print("❌ No standardized food_place_dishes files found.")
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

output_file = (
    COMBINED_DIR / "food_place_dishes.csv"
)

combined_df.to_csv(
    output_file,
    index=False
)

print("\n============================================")
print(f"Files combined: {len(files)}")
print(f"Total rows: {len(combined_df)}")
print(
    f"Unique link IDs: "
    f"{combined_df['link_id'].nunique()}"
)
print(f"Saved to: {output_file}")
print("============================================")

if len(combined_df) == combined_df["link_id"].nunique():
    print("\n✅ All link_id values remain unique.")
else:
    print("\n⚠️ Duplicate link_id values exist.")