from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

STANDARDIZED_DIR = (
    BASE_DIR / "standardized" / "social_recommendations"
)

COMBINED_DIR = BASE_DIR / "combined"
FOOD_PLACES_FILE = COMBINED_DIR / "food_places.csv"

EXPECTED_COLUMNS = [
    "signal_id",
    "platform",
    "place_id",
    "place_name",
    "food_or_topic",
    "signal_polarity",
    "signal_type",
    "structured_summary",
    "local_vs_tourist_signal",
    "source_url",
    "verified_date",
    "confidence",
]

print("\n========== SOCIAL RECOMMENDATIONS VALIDATION ==========\n")

files = list(
    STANDARDIZED_DIR.glob("*_social_recommendations.csv")
)

if not files:
    print("❌ No standardized social recommendation files found.")
    raise SystemExit

print(f"Found {len(files)} standardized files.\n")

# Load food_places so we can validate place_id where available
food_places = pd.read_csv(FOOD_PLACES_FILE)

valid_place_ids = set(
    food_places["place_id"]
    .dropna()
    .astype(str)
)

all_rows = []
all_signal_ids = []
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
        "signal_id",
        "place_name",
        "structured_summary",
    ]:
        missing = df[column].isna().sum()

        if missing == 0:
            print(f"✅ No missing {column}")
        else:
            print(f"⚠️ Missing {column}: {missing}")

    # 3. Duplicate signal_id inside file
    duplicate_ids = df["signal_id"].duplicated().sum()

    if duplicate_ids == 0:
        print("✅ No duplicate signal_id inside file")
    else:
        print(
            f"❌ Duplicate signal_id inside file: "
            f"{duplicate_ids}"
        )

    all_signal_ids.extend(
        df["signal_id"]
        .dropna()
        .astype(str)
        .tolist()
    )

    # 4. Validate place_id only when it exists
    rows_with_place_id = df[
        df["place_id"].notna()
    ].copy()

    if not rows_with_place_id.empty:

        invalid_places = rows_with_place_id[
            ~rows_with_place_id["place_id"]
            .astype(str)
            .isin(valid_place_ids)
        ]

        if invalid_places.empty:
            print("✅ All available place_id references are valid")
        else:
            print(
                f"❌ Invalid place_id references: "
                f"{len(invalid_places)}"
            )

            print(
                invalid_places[
                    [
                        "signal_id",
                        "place_id",
                        "place_name"
                    ]
                ].to_string(index=False)
            )
    else:
        print("ℹ️ No place_id values available in this file")

    # 5. Confidence range
    confidence = pd.to_numeric(
        df["confidence"],
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


# Global checks
combined = pd.concat(
    all_rows,
    ignore_index=True
)

print("\n" + "=" * 70)
print("GLOBAL SIGNAL ID CHECK")
print("=" * 70)

signal_series = pd.Series(all_signal_ids)

duplicate_global_ids = signal_series[
    signal_series.duplicated(keep=False)
]

if duplicate_global_ids.empty:
    print("✅ All signal_id values are globally unique")
else:
    print(
        f"⚠️ Duplicate signal_id values found: "
        f"{duplicate_global_ids.nunique()} unique duplicated IDs"
    )

    print(
        duplicate_global_ids
        .value_counts()
        .head(30)
        .to_string()
    )


print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"Files found: {len(files)}")
print(f"Files with correct schema: {valid_files}")
print(f"Total social recommendation rows: {len(combined)}")
print(
    f"Unique signal IDs: "
    f"{combined['signal_id'].nunique()}"
)