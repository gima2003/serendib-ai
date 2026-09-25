from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. Folder locations
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
STANDARDIZED_DIR = BASE_DIR / "standardized"


# ---------------------------------------------------------
# 2. Standard category mapping
# ---------------------------------------------------------

CATEGORY_MAP = {

    # Heritage
    "Archaeological / Heritage Site": "Heritage",
    "Archaeological Site": "Heritage",
    "Historic Site": "Heritage",
    "Historic / Scenic": "Heritage",
    "Island / Heritage": "Heritage",
    "Mountain / Archaeology": "Heritage",
    "Mountain / Heritage": "Heritage",
    "Nature / Heritage": "Heritage",
    "Railway Heritage": "Heritage",
    "Heritage / Leisure Complex": "Heritage",

    # Religious
    "Religious Site": "Religious",
    "Religious / Archaeological Site": "Religious",
    "Religious / Heritage Site": "Religious",
    "Religious / Historic Site": "Religious",
    "Religious / Nature Site": "Religious",
    "Religious / Viewpoint": "Religious",
    "Cave / Religious": "Religious",

    # Nature
    "Waterfall": "Nature",
    "Forest Reserve": "Nature",
    "Botanical Garden": "Nature",
    "Mountain / Viewpoint": "Nature",
    "Cave / Natural Pool": "Nature",
    "Lake / Scenic": "Nature",
    "Farm": "Nature",

    # Wildlife
    "National Park": "Wildlife",
    "Zoological Garden": "Wildlife",

    # Beach & Marine
    "Beach": "Beach & Marine",
    "Beach / Nature": "Beach & Marine",
    "Beach / Surf": "Beach & Marine",
    "Coastal Viewpoint": "Beach & Marine",
    "Viewpoint / Coastal": "Beach & Marine",
    "Marine Wildlife Experience": "Beach & Marine",
    "Surf Break": "Beach & Marine",

    # Adventure
    "Viewpoint / Tea Country": "Adventure",

    # Museum & Culture
    "Museum": "Museum & Culture",
    "Cultural Landmark": "Museum & Culture",

    # Scenic & Leisure
    "Viewpoint": "Scenic & Leisure",
    "Lake / Recreation": "Scenic & Leisure",
    "Urban Park / Garden": "Scenic & Leisure",
    "Urban Park / Seafront": "Scenic & Leisure",
    "Landmark": "Scenic & Leisure",
    "Landmark / Observation Tower": "Scenic & Leisure",

    # Local Experience
    "Tea Estate": "Local Experience",
    "Tea Estate / Factory": "Local Experience",

    # Urban & Shopping
    "Market": "Urban & Shopping",
}


# ---------------------------------------------------------
# 3. Helper functions
# ---------------------------------------------------------

def clean_text(value):
    """
    Remove unnecessary spaces from text values.
    """

    if pd.isna(value):
        return value

    return " ".join(str(value).strip().split())


def clean_source_ids(value):
    """
    Standardize multiple source IDs.

    Example:
    SRC001 | SRC002
    SRC001|SRC002

    becomes:
    SRC001|SRC002
    """

    if pd.isna(value):
        return value

    parts = [
        part.strip()
        for part in str(value).split("|")
        if part.strip()
    ]

    return "|".join(parts)


def clean_primary_activity(value):
    """
    Standardize activity separators.

    Example:
    Hiking|Photography
    Hiking | Photography

    becomes:
    Hiking | Photography
    """

    if pd.isna(value):
        return value

    parts = [
        part.strip()
        for part in str(value).split("|")
        if part.strip()
    ]

    return " | ".join(parts)


# ---------------------------------------------------------
# 4. Standardize one attraction file
# ---------------------------------------------------------

def standardize_file(file_path):

    df = pd.read_csv(file_path)

    # Preserve original detailed category
    df["sub_category"] = df["category"]

    # Convert detailed category into broad category
    df["category"] = df["category"].map(
        CATEGORY_MAP
    ).fillna("Other")

    # Clean text columns
    text_columns = [
        "attraction_id",
        "attraction_name",
        "city",
        "district",
        "province",
        "description",
        "sub_category",
    ]

    for column in text_columns:
        df[column] = df[column].apply(clean_text)

    # Standardize IDs to uppercase
    df["attraction_id"] = (
        df["attraction_id"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # Clean source IDs
    df["source_id"] = (
        df["source_id"]
        .apply(clean_source_ids)
    )

    # Clean activity field
    df["primary_activity"] = (
        df["primary_activity"]
        .apply(clean_primary_activity)
    )

    # Convert date into standard ISO format
    df["verified_date"] = pd.to_datetime(
        df["verified_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Reorder columns
    column_order = [
        "attraction_id",
        "attraction_name",
        "city",
        "district",
        "province",
        "category",
        "sub_category",
        "description",
        "primary_activity",
        "source_id",
        "verified_date",
    ]

    df = df[column_order]

    return df


# ---------------------------------------------------------
# 5. Process all city attraction datasets
# ---------------------------------------------------------

def main():

    print("\n==========================================")
    print("SERENDIB AI - AGENT 2 STANDARDIZATION")
    print("==========================================\n")

    attraction_files = sorted(
        RAW_DIR.rglob("*_attractions.csv")
    )

    if not attraction_files:
        print("No raw attraction CSV files found.")
        return

    STANDARDIZED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    total_files = 0
    total_rows = 0

    for file_path in attraction_files:

        standardized_df = standardize_file(
            file_path
        )

        file_name = file_path.name

        output_path = (
            STANDARDIZED_DIR / file_name
        )

        standardized_df.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig"
        )

        total_files += 1
        total_rows += len(standardized_df)

        print(
            f"[OK] {file_name} "
            f"-> {len(standardized_df)} attractions"
        )

    print("\n==========================================")
    print("STANDARDIZATION SUMMARY")
    print("==========================================")

    print(f"Files processed     : {total_files}")
    print(f"Attractions cleaned : {total_rows}")

    print(
        f"\nStandardized files saved to:\n"
        f"{STANDARDIZED_DIR}"
    )


if __name__ == "__main__":
    main()