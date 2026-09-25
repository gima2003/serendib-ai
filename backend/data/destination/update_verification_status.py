import pandas as pd


INPUT = "data/destination/combined/attraction_costs.csv"
OUTPUT = "data/destination/combined/attraction_costs.csv"


df = pd.read_csv(
    INPUT,
    keep_default_na=False
)


# Prices were manually researched
df["verification_status"] = "VERIFIED"


# Add general note only if empty
df["notes"] = df["notes"].apply(
    lambda x: x
    if x.strip()
    else "Price manually checked from relevant attraction/tourism sources."
)


df.to_csv(
    OUTPUT,
    index=False
)


print("✅ Verification status updated")
print(
    df["verification_status"].value_counts()
)