from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

print("\n========== EVALUATION QUERIES SCHEMA CHECK ==========\n")

files = list(RAW_DIR.rglob("evaluation_queries.csv"))

if not files:
    print("❌ No evaluation_queries.csv files found.")
    raise SystemExit

print(f"Found {len(files)} evaluation_queries files.\n")

total_rows = 0

for file_path in files:

    print("-" * 70)
    print(f"📄 {file_path.relative_to(BASE_DIR)}")

    try:
        df = pd.read_csv(file_path)

        total_rows += len(df)

        print(f"Rows: {len(df)}")
        print("Columns:")

        for column in df.columns:
            print(f"  - {column}")

    except Exception as e:
        print(f"❌ Error reading file: {e}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"Files found: {len(files)}")
print(f"Total rows: {total_rows}")

print("\n========== FINISHED ==========")