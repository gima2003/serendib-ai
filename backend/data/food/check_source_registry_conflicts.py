from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
STANDARDIZED_DIR = BASE_DIR / "standardized" / "source_registry"

print("\n========== SOURCE REGISTRY CONFLICT CHECK ==========\n")

files = list(
    STANDARDIZED_DIR.glob("*_source_registry.csv")
)

if not files:
    print("❌ No standardized source registry files found.")
    raise SystemExit

all_rows = []

for file_path in files:
    df = pd.read_csv(file_path)

    df["source_file"] = file_path.name

    # Normalize URL for comparison
    df["normalized_url"] = (
        df["source_url"]
        .astype(str)
        .str.strip()
        .str.rstrip("/")
        .str.lower()
    )

    all_rows.append(df)

combined = pd.concat(
    all_rows,
    ignore_index=True
)

duplicate_urls = combined[
    combined["normalized_url"].duplicated(keep=False)
]

if duplicate_urls.empty:
    print("✅ No duplicate source URLs found.")
    raise SystemExit


print(
    f"Repeated URLs: "
    f"{duplicate_urls['normalized_url'].nunique()}\n"
)


for url, group in duplicate_urls.groupby("normalized_url"):

    print("=" * 80)
    print(f"URL: {url}")

    print(f"Occurrences: {len(group)}")

    print("\nSource types:")
    for value in group["source_type"].dropna().unique():
        print(f"  - {value}")

    print("\nSource names:")
    for value in group["source_name"].dropna().unique():
        print(f"  - {value}")

    print("\nRecommended uses:")
    for value in group["recommended_use"].dropna().unique():
        print(f"  - {value}")

    print("\nDefault confidence:")
    for value in group["default_confidence"].dropna().unique():
        print(f"  - {value}")

    print("\nAppears in:")
    for value in group["source_file"].unique():
        print(f"  - {value}")


print("\n========== SUMMARY ==========")
print(f"Total source rows: {len(combined)}")
print(
    f"Unique normalized URLs: "
    f"{combined['normalized_url'].nunique()}"
)
print(
    f"URLs appearing more than once: "
    f"{duplicate_urls['normalized_url'].nunique()}"
)