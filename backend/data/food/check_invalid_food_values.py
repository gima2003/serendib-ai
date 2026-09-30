from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

print("\n========== CHECKING INVALID FOOD VALUES ==========\n")

food_place_files = list(RAW_DIR.rglob("food_places.csv"))

for file_path in food_place_files:
    df = pd.read_csv(file_path)

    # Check rating
    if "rating" in df.columns:
        rating_numeric = pd.to_numeric(df["rating"], errors="coerce")

        invalid_rating_mask = (
            rating_numeric.notna()
            & ((rating_numeric < 0) | (rating_numeric > 5))
        )

        invalid_ratings = df[invalid_rating_mask]

        if not invalid_ratings.empty:
            print(f"\n📄 {file_path.relative_to(BASE_DIR)}")
            print("⚠️ Invalid rating rows:")

            columns_to_show = [
                col for col in [
                    "place_id",
                    "place_name",
                    "city",
                    "rating",
                    "source_url"
                ]
                if col in df.columns
            ]

            print(
                invalid_ratings[columns_to_show]
                .to_string(index=False)
            )

print("\nFinished.")