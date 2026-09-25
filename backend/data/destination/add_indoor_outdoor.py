import pandas as pd


INPUT = "data/destination/combined/attractions.csv"
OUTPUT = "data/destination/combined/attractions.csv"


df = pd.read_csv(INPUT)


# Add new column
df["indoor_outdoor"] = ""


df.to_csv(
    OUTPUT,
    index=False
)


print("✅ indoor_outdoor column added")
print(df.columns)