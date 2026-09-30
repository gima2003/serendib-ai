from pathlib import Path
import os
import pandas as pd

from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent.parent

load_dotenv(BACKEND_DIR / ".env")

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

CSV_FILE = BASE_DIR / "combined" / "food_items.csv"

print("\n========== IMPORT FOOD ITEMS TO MONGODB ==========\n")

df = pd.read_csv(CSV_FILE)

print("✅ CSV loaded")
print(f"Rows found: {len(df)}")

df = df.where(pd.notnull(df), None)

records = df.to_dict(orient="records")

client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=10000
)

client.admin.command("ping")

print("✅ MongoDB connection successful")

db = client[DATABASE_NAME]
collection = db["food_items"]

existing_count = collection.count_documents({})

print(f"Existing records in food_items: {existing_count}")

if existing_count > 0:
    collection.delete_many({})
    print("✅ Old food_items records removed")

if records:
    result = collection.insert_many(records)
    print(f"✅ Inserted {len(result.inserted_ids)} records")
else:
    print("❌ No records found to insert")

final_count = collection.count_documents({})

print("\n========== IMPORT SUMMARY ==========")
print(f"Database: {DATABASE_NAME}")
print("Collection: food_items")
print(f"Final record count: {final_count}")

if final_count == len(df):
    print("\n✅ MongoDB import completed successfully.")
else:
    print("\n⚠️ Record count does not match CSV.")

client.close()