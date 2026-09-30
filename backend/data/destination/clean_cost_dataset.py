import pandas as pd


INPUT = "data/destination/combined/attraction_costs.csv"
OUTPUT = "data/destination/combined/attraction_costs.csv"


df = pd.read_csv(INPUT)


# Replace missing boolean values
df["requires_live_check"] = (
    df["requires_live_check"]
    .fillna(False)
)


# Replace missing text values
text_columns = [
    "price_type",
    "source_authority",
    "source_url",
    "last_verified",
    "notes"
]


for col in text_columns:
    df[col] = df[col].fillna("")


df.to_csv(
    OUTPUT,
    index=False
)


print("✅ Cost dataset cleaned successfully")