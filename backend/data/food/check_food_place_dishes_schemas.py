from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

print("\n========== FOOD PLACE DISHES SCHEMA CHECK ==========\n")

files = list(RAW_DIR.rglob("food_place_dishes.csv"))

if not files:
    print("❌ No food_place_dishes.csv files found.")
    raise SystemExit

print(f"Found {len(files)} food_place_dishes files.\n")

for file_path in files:
    print("-" * 70)
    print(f"📄 {file_path.relative_to(BASE_DIR)}")

    try:
        df = pd.read_csv(file_path)

        print(f"Rows: {len(df)}")
        print("Columns:")

        for col in df.columns:
            print(f"  - {col}")

    except Exception as e:
        print(f"❌ Error reading file: {e}")

print("\n========== FINISHED ==========")