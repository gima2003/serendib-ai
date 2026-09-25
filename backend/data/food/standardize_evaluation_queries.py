from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

OUTPUT_DIR = (
    BASE_DIR / "standardized" / "evaluation_queries"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_COLUMNS = [
    "query_id",
    "city",
    "sample_user_query",
    "expected_filters_or_intent",
    "relevant_place_ids",
    "expected_result_text",
    "notes",
]

CITY_NAMES = {
    "arugam_bay": "Arugam Bay",
    "bandarawela": "Bandarawela",
    "colombo": "Colombo",
    "dambulla": "Dambulla",
    "ella": "Ella",
    "galle": "Galle",
    "jaffna": "Jaffna",
    "kandy": "Kandy",
    "mirissa": "Mirissa",
    "nuwara_eliya": "Nuwara Eliya",
    "sigiriya": "Sigiriya",
    "yala": "Yala",
}

print("\n========== STANDARDIZING EVALUATION QUERIES ==========\n")

for city_folder, city_name in CITY_NAMES.items():

    city_dir = RAW_DIR / city_folder

    files = list(
        city_dir.rglob("evaluation_queries.csv")
    )

    if not files:
        print(
            f"⚠️ No evaluation_queries.csv found "
            f"for {city_name}"
        )
        continue

    file_path = files[0]

    print(f"\n📄 Processing {city_name}")

    df = pd.read_csv(file_path)

    # ------------------------------
    # Normalize query text
    # ------------------------------

    if "query" in df.columns:
        df = df.rename(
            columns={
                "query": "sample_user_query"
            }
        )

    # ------------------------------
    # Normalize expected place IDs
    # ------------------------------

    if "expected_places" in df.columns:
        df = df.rename(
            columns={
                "expected_places": "relevant_place_ids"
            }
        )

    # ------------------------------
    # Normalize text expectations
    # ------------------------------

    if "expected_result" in df.columns:
        df = df.rename(
            columns={
                "expected_result": "expected_result_text"
            }
        )

    if "expected" in df.columns:
        df = df.rename(
            columns={
                "expected": "expected_result_text"
            }
        )

    # ------------------------------
    # Add city
    # ------------------------------

    df["city"] = city_name

    # ------------------------------
    # Generate missing query IDs
    # ------------------------------

    if "query_id" not in df.columns:

        prefix_map = {
            "arugam_bay": "ABY",
            "bandarawela": "BDR",
            "colombo": "COL",
            "dambulla": "DAM",
            "ella": "ELL",
            "galle": "GAL",
            "jaffna": "JAF",
            "kandy": "KDY",
            "mirissa": "MIR",
            "nuwara_eliya": "NEL",
            "sigiriya": "SIG",
            "yala": "YAL",
        }

        prefix = prefix_map[city_folder]

        df["query_id"] = [
            f"{prefix}-Q{i:03d}"
            for i in range(1, len(df) + 1)
        ]

    else:

        prefix_map = {
            "arugam_bay": "ABY",
            "bandarawela": "BDR",
            "colombo": "COL",
            "dambulla": "DAM",
            "ella": "ELL",
            "galle": "GAL",
            "jaffna": "JAF",
            "kandy": "KDY",
            "mirissa": "MIR",
            "nuwara_eliya": "NEL",
            "sigiriya": "SIG",
            "yala": "YAL",
        }

        prefix = prefix_map[city_folder]

        df["query_id"] = (
            df["query_id"]
            .astype(str)
            .apply(
                lambda x: (
                    f"{prefix}-{x}"
                    if not x.startswith(f"{prefix}-")
                    else x
                )
            )
        )

    # ------------------------------
    # Add missing master columns
    # ------------------------------

    for column in MASTER_COLUMNS:
        if column not in df.columns:
            df[column] = None

    # ------------------------------
    # Reorder
    # ------------------------------

    df = df[MASTER_COLUMNS]

    output_file = (
        OUTPUT_DIR
        / f"{city_folder}_evaluation_queries.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"✅ Saved {output_file.name} "
        f"({len(df)} rows)"
    )

print("\n========== FINISHED ==========")