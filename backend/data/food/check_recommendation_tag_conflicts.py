from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

print("\n========== RECOMMENDATION TAG DEFINITION CHECK ==========\n")

files = list(RAW_DIR.rglob("recommendation_tags.csv"))

all_rows = []

for file_path in files:
    df = pd.read_csv(file_path)

    # Add source file so we can see where each version came from
    df["source_file"] = str(file_path.relative_to(BASE_DIR))

    all_rows.append(df)

combined = pd.concat(
    all_rows,
    ignore_index=True
)

# Normalize tag names slightly for comparison
combined["tag_normalized"] = (
    combined["tag"]
    .astype(str)
    .str.strip()
    .str.lower()
)

print(f"Total rows: {len(combined)}")
print(f"Unique normalized tags: {combined['tag_normalized'].nunique()}")

print("\n========== TAGS WITH MULTIPLE DEFINITIONS ==========\n")

conflict_count = 0

for tag, group in combined.groupby("tag_normalized"):

    unique_definitions = (
        group["definition"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    if len(unique_definitions) > 1:

        conflict_count += 1

        print("-" * 70)
        print(f"⚠️ Tag: {tag}")
        print(f"Different definitions: {len(unique_definitions)}")

        for definition in unique_definitions:
            print(f"   - {definition}")

        print("Used in:")
        for source in group["source_file"].unique():
            print(f"   {source}")

if conflict_count == 0:
    print("✅ No conflicting definitions found.")

print("\n========== SUMMARY ==========")
print(f"Unique tags: {combined['tag_normalized'].nunique()}")
print(f"Tags with conflicting definitions: {conflict_count}")