from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
STANDARDIZED_DIR = BASE_DIR / "standardized" / "source_registry"
COMBINED_DIR = BASE_DIR / "combined"

COMBINED_DIR.mkdir(exist_ok=True)

print("\n========== BUILDING MASTER SOURCE REGISTRY ==========\n")

files = list(
    STANDARDIZED_DIR.glob("*_source_registry.csv")
)

if not files:
    print("❌ No standardized source registry files found.")
    raise SystemExit

all_rows = []

for file_path in files:
    df = pd.read_csv(file_path)

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

print(f"Original rows: {len(combined)}")
print(
    f"Unique normalized URLs: "
    f"{combined['normalized_url'].nunique()}"
)


def join_unique(series):
    values = (
        series
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = [
        value
        for value in values
        if value
    ]

    unique_values = list(dict.fromkeys(values))

    return " | ".join(unique_values) if unique_values else None


def conservative_confidence(series):
    values = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if values.empty:
        return None

    # Use the lowest confidence when duplicate
    # records disagree.
    return float(values.min())


master_rows = []

for index, (url, group) in enumerate(
    combined.groupby("normalized_url"),
    start=1
):

    # Preserve the original URL format from first record
    source_url = (
        group["source_url"]
        .dropna()
        .astype(str)
        .str.strip()
        .iloc[0]
    )

    source_type = join_unique(
        group["source_type"]
    )

    source_name = join_unique(
        group["source_name"]
    )

    recommended_use = join_unique(
        group["recommended_use"]
    )

    default_confidence = conservative_confidence(
        group["default_confidence"]
    )

    master_rows.append({
        "source_id": f"SRC-{index:03d}",
        "source_type": source_type,
        "source_name": source_name,
        "source_url": source_url,
        "recommended_use": recommended_use,
        "default_confidence": default_confidence,
    })


master_df = pd.DataFrame(master_rows)

output_file = (
    COMBINED_DIR / "source_registry.csv"
)

master_df.to_csv(
    output_file,
    index=False
)


print("\n========== MASTER SOURCE SUMMARY ==========")

print(f"Original rows: {len(combined)}")
print(f"Master rows: {len(master_df)}")
print(
    f"Unique source IDs: "
    f"{master_df['source_id'].nunique()}"
)
print(
    f"Unique source URLs: "
    f"{master_df['source_url'].nunique()}"
)

print(f"\nSaved to: {output_file}")

if (
    len(master_df)
    == master_df["source_id"].nunique()
    and
    len(master_df)
    == master_df["source_url"].nunique()
):
    print(
        "\n✅ Master source registry created successfully."
    )
else:
    print(
        "\n⚠️ Duplicate source IDs or URLs remain."
    )