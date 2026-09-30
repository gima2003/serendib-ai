from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

print("\n========== RECOMMENDATION TAGS VALIDATION ==========\n")

files = list(RAW_DIR.rglob("recommendation_tags.csv"))

if not files:
    print("❌ No recommendation_tags.csv files found.")
    raise SystemExit

all_rows = []

for file_path in files:
    df = pd.read_csv(file_path)

    print("-" * 70)
    print(f"📄 {file_path.relative_to(BASE_DIR)}")
    print(f"Rows: {len(df)}")

    # Schema
    expected = ["tag_id", "tag", "definition"]

    if list(df.columns) == expected:
        print("✅ Schema correct")
    else:
        print("❌ Schema mismatch")

    # Missing values
    for column in expected:
        missing = df[column].isna().sum()

        if missing == 0:
            print(f"✅ No missing {column}")
        else:
            print(f"⚠️ Missing {column}: {missing}")

    all_rows.append(df)


combined = pd.concat(all_rows, ignore_index=True)

print("\n" + "=" * 70)
print("GLOBAL TAG CHECK")
print("=" * 70)

# Duplicate tag_id
duplicate_ids = combined[
    combined["tag_id"].duplicated(keep=False)
]

if duplicate_ids.empty:
    print("✅ All tag_id values are unique")
else:
    print(
        f"⚠️ Duplicate tag_id values found: "
        f"{duplicate_ids['tag_id'].nunique()} unique duplicated IDs"
    )

# Duplicate tag names
duplicate_tags = combined[
    combined["tag"].duplicated(keep=False)
]

if duplicate_tags.empty:
    print("✅ All tag names are unique")
else:
    print(
        f"⚠️ Duplicate tag names found: "
        f"{duplicate_tags['tag'].nunique()} repeated tag names"
    )

    print("\nRepeated tag names:")
    print(
        duplicate_tags["tag"]
        .value_counts()
        .to_string()
    )

print("\n========== SUMMARY ==========")
print(f"Files found: {len(files)}")
print(f"Total rows across files: {len(combined)}")
print(f"Unique tag IDs: {combined['tag_id'].nunique()}")
print(f"Unique tag names: {combined['tag'].nunique()}")