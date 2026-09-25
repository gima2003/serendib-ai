import pandas as pd


FILE = "data/destination/combined/attraction_costs.csv"


df = pd.read_csv(FILE)


print("==============================")
print("ATTRACTION COST DATASET CHECK")
print("==============================")


print("Rows:", len(df))
print("Columns:")
print(df.columns.tolist())


print("\nMissing values:")
print(df.isnull().sum())


print("\nSample:")
print(df.head())