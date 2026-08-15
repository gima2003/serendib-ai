from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
STANDARDIZED_DIR = BASE_DIR / "standardized" / "source_registry"

EXPECTED_COLUMNS = [
    "source_id",
    "source_type",
    "source_name",
    "source_url",
    "recommended_use",
    "default_confidence",
]

print("\n========== SOURCE REGISTRY VALIDATION ==========\n")

files = list(
    STANDARDIZED_DIR.glob("*_source_registry.csv")
)

if not files:
    print("❌ No standardized source_registry files found.")
    raise SystemExit

print(f"Found {len(files)} standardized source registry files.\n")

all_rows = []
valid_files = 0

for file_path in files:

    print("-" * 70)
    print(f"📄 {file_path.name}")

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df)}")

    # 1. Schema
    if list(df.columns) == EXPECTED_COLUMNS:
        print("✅ Schema correct")
        valid_files += 1
    else:
        print("❌ Schema mismatch")

    # 2. Critical fields
    for column in [
        "source_id",
        "source_type",
        "source_url",
    ]:
        missing = df[column].isna().sum()

        if missing == 0:
            print(f"✅ No missing {column}")
        else:
            print(f"⚠️ Missing {column}: {missing}")

    # 3. Duplicate source IDs inside file
    duplicate_ids = df["source_id"].duplicated().sum()

    if duplicate_ids == 0:
        print("✅ No duplicate source_id inside file")
    else:
        print(
            f"❌ Duplicate source_id inside file: "
            f"{duplicate_ids}"
        )

    # 4. Confidence range
    confidence = pd.to_numeric(
        df["default_confidence"],
        errors="coerce"
    )

    invalid_confidence = confidence[
        confidence.notna()
        & (
            (confidence < 0)
            | (confidence > 1)
        )
    ]

    if len(invalid_confidence) == 0:
        print("✅ Confidence values valid or empty")
    else:
        print(
            f"⚠️ Confidence outside 0–1: "
            f"{len(invalid_confidence)}"
        )

    all_rows.append(df)


# --------------------------------------
# Global checks
# --------------------------------------

combined = pd.concat(
    all_rows,
    ignore_index=True
)

print("\n" + "=" * 70)
print("GLOBAL SOURCE CHECK")
print("=" * 70)

# Duplicate source IDs
duplicate_global_ids = combined[
    combined["source_id"].duplicated(keep=False)
]

if duplicate_global_ids.empty:
    print("✅ All source_id values are globally unique")
else:
    print(
        f"⚠️ Duplicate source_id values found: "
        f"{duplicate_global_ids['source_id'].nunique()}"
    )

# Duplicate URLs
valid_urls = combined[
    combined["source_url"].notna()
].copy()

duplicate_urls = valid_urls[
    valid_urls["source_url"].duplicated(keep=False)
]

if duplicate_urls.empty:
    print("✅ No duplicate source URLs")
else:
    print(
        f"⚠️ Duplicate source URLs found: "
        f"{duplicate_urls['source_url'].nunique()}"
    )

    print("\nMost repeated source URLs:")

    print(
        duplicate_urls["source_url"]
        .value_counts()
        .head(20)
        .to_string()
    )


print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"Files found: {len(files)}")
print(f"Files with correct schema: {valid_files}")
print(f"Total source rows: {len(combined)}")
print(
    f"Unique source IDs: "
    f"{combined['source_id'].nunique()}"
)
print(
    f"Unique source URLs: "
    f"{combined['source_url'].nunique()}"
)