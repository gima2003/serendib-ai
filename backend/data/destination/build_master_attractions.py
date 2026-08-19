from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. Folder locations
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

STANDARDIZED_DIR = BASE_DIR / "standardized"
COMBINED_DIR = BASE_DIR / "combined"

OUTPUT_FILE = COMBINED_DIR / "attractions.csv"


# ---------------------------------------------------------
# 2. Expected final column order
# ---------------------------------------------------------

EXPECTED_COLUMNS = [
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


# ---------------------------------------------------------
# 3. Load all standardized attraction files
# ---------------------------------------------------------

def load_standardized_files():

    attraction_files = sorted(
        STANDARDIZED_DIR.glob("*_attractions.csv")
    )

    if not attraction_files:
        raise FileNotFoundError(
            f"No standardized attraction files found in:\n"
            f"{STANDARDIZED_DIR}"
        )

    dataframes = []

    for file_path in attraction_files:

        df = pd.read_csv(file_path)

        # Check column structure
        missing_columns = [
            column
            for column in EXPECTED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{file_path.name} is missing columns: "
                f"{', '.join(missing_columns)}"
            )

        # Keep columns in the correct order
        df = df[EXPECTED_COLUMNS]

        dataframes.append(df)

        print(
            f"[LOADED] {file_path.name} "
            f"- {len(df)} attractions"
        )

    return dataframes


# ---------------------------------------------------------
# 4. Build one master dataframe
# ---------------------------------------------------------

def build_master_dataframe(dataframes):

    master_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    # -----------------------------------------------------
    # Check duplicate attraction IDs
    # -----------------------------------------------------

    duplicate_ids = master_df[
        master_df["attraction_id"].duplicated(
            keep=False
        )
    ]

    if not duplicate_ids.empty:

        print("\nDuplicate attraction IDs found:")

        print(
            duplicate_ids[
                [
                    "attraction_id",
                    "attraction_name",
                    "city"
                ]
            ]
        )

        raise ValueError(
            "Master dataset contains duplicate "
            "attraction IDs."
        )

    # -----------------------------------------------------
    # Check important missing values
    # -----------------------------------------------------

    important_columns = [
        "attraction_id",
        "attraction_name",
        "city",
        "category",
        "description",
    ]

    for column in important_columns:

        missing_count = (
            master_df[column]
            .isna()
            .sum()
        )

        if missing_count > 0:

            raise ValueError(
                f"Column '{column}' contains "
                f"{missing_count} missing value(s)."
            )

    # -----------------------------------------------------
    # Sort data
    # -----------------------------------------------------

    master_df = master_df.sort_values(
        by=[
            "city",
            "attraction_name"
        ]
    ).reset_index(drop=True)

    return master_df


# ---------------------------------------------------------
# 5. Save combined attractions.csv
# ---------------------------------------------------------

def save_master_dataset(master_df):

    COMBINED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    master_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n==========================================")
    print("MASTER ATTRACTIONS DATASET CREATED")
    print("==========================================")

    print(
        f"Total attractions : {len(master_df)}"
    )

    print(
        f"Unique IDs        : "
        f"{master_df['attraction_id'].nunique()}"
    )

    print(
        f"Cities            : "
        f"{master_df['city'].nunique()}"
    )

    print(
        f"Categories        : "
        f"{master_df['category'].nunique()}"
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )


# ---------------------------------------------------------
# 6. Main program
# ---------------------------------------------------------

def main():

    print("\n==========================================")
    print("SERENDIB AI - BUILD MASTER ATTRACTIONS")
    print("==========================================\n")

    try:

        dataframes = load_standardized_files()

        master_df = build_master_dataframe(
            dataframes
        )

        save_master_dataset(
            master_df
        )

    except Exception as error:

        print("\n[ERROR]")
        print(error)

        print(
            "\nMaster attractions dataset "
            "was NOT created."
        )


if __name__ == "__main__":
    main()