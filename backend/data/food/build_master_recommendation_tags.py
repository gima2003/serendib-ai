from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
COMBINED_DIR = BASE_DIR / "combined"

COMBINED_DIR.mkdir(exist_ok=True)

print("\n========== BUILDING MASTER RECOMMENDATION TAGS ==========\n")

files = list(RAW_DIR.rglob("recommendation_tags.csv"))

if not files:
    print("❌ No recommendation_tags.csv files found.")
    raise SystemExit

all_rows = []

for file_path in files:
    df = pd.read_csv(file_path)

    df["tag_normalized"] = (
        df["tag"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    all_rows.append(df)

combined = pd.concat(
    all_rows,
    ignore_index=True
)

print(f"Original rows: {len(combined)}")
print(
    f"Unique tags: "
    f"{combined['tag_normalized'].nunique()}"
)


# ------------------------------------------------
# Canonical definitions for conflicting common tags
# ------------------------------------------------

CANONICAL_DEFINITIONS = {

    "authentic-local":
        "Strong orientation toward authentic Sri Lankan local food.",

    "beach-dining":
        "Beachfront or beach-oriented dining experience.",

    "breakfast":
        "Suitable for breakfast or morning meal recommendations.",

    "budget":
        "Suitable for affordable or lower-cost casual dining.",

    "cooking-class":
        "Includes a hands-on food preparation or cooking experience.",

    "family":
        "Suitable for family-friendly dining.",

    "fresh-catch":
        "Strong indication of freshly caught fish or seafood.",

    "healthy":
        "Health-conscious, vegetable-forward, organic, or plant-based dining.",

    "hill-country":
        "Relevant to Sri Lanka's hill-country or highland food experience.",

    "home-style":
        "Home-style or family-style Sri Lankan food experience.",

    "hotel":
        "Dining available at or associated with a hotel.",

    "late-night":
        "Suitable for later evening or late-night dining.",

    "mixed-group":
        "Suitable for groups with both local and international food preferences.",

    "roti":
        "Roti is a core, signature, or strongly recommended food item.",

    "scenic":
        "The view or surrounding setting is an important part of the dining experience.",

    "seafood":
        "Strong focus on seafood dishes or seafood dining.",

    "tea":
        "Relevant to tea or tea-country food and drink experiences.",

    "tourist-popular":
        "Highly visible or frequently reviewed by travellers.",

    "vegan-friendly":
        "Offers or is reported to offer suitable vegan options.",

    "vegetarian":
        "Suitable for vegetarian dining or filtering.",

    "village-food":
        "Traditional village-style or home-style local food experience.",
}


# ------------------------------------------------
# Build one row per unique tag
# ------------------------------------------------

master_rows = []

unique_tags = sorted(
    combined["tag_normalized"].unique()
)

for index, tag in enumerate(unique_tags, start=1):

    group = combined[
        combined["tag_normalized"] == tag
    ]

    # Use our canonical definition when required.
    if tag in CANONICAL_DEFINITIONS:
        definition = CANONICAL_DEFINITIONS[tag]

    else:
        # For non-conflicting tags, preserve an existing definition.
        definition = (
            group["definition"]
            .dropna()
            .astype(str)
            .str.strip()
            .iloc[0]
        )

    master_rows.append({
        "tag_id": f"TAG-{index:03d}",
        "tag": tag,
        "definition": definition
    })


master_df = pd.DataFrame(master_rows)

output_file = (
    COMBINED_DIR / "recommendation_tags.csv"
)

master_df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------
# Final checks
# ------------------------------------------------

print("\n========== MASTER TAG SUMMARY ==========")

print(f"Original rows: {len(combined)}")
print(f"Master rows: {len(master_df)}")
print(
    f"Unique tags: "
    f"{master_df['tag'].nunique()}"
)
print(
    f"Unique tag IDs: "
    f"{master_df['tag_id'].nunique()}"
)

print(f"\nSaved to: {output_file}")

if (
    len(master_df) == master_df["tag"].nunique()
    and
    len(master_df) == master_df["tag_id"].nunique()
):
    print(
        "\n✅ Master recommendation tag dictionary "
        "created successfully."
    )
else:
    print(
        "\n❌ Duplicate tags or IDs remain."
    )