from pathlib import Path
import os
import pandas as pd

from dotenv import load_dotenv
from pymongo import MongoClient

# -----------------------------------------
# 1. Load environment variables
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent.parent

load_dotenv(BACKEND_DIR / ".env")

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# -----------------------------------------
# 2. File path
# -----------------------------------------

CSV_FILE = BASE_DIR / "combined" / "food_places.csv"

print("\n========== IMPORT FOOD PLACES TO MONGODB ==========\n")

# -----------------------------------------
# 3. Read CSV
# -----------------------------------------

df = pd.read_csv(CSV_FILE)

print(f"✅ CSV loaded")
print(f"Rows found: {len(df)}")

# Replace NaN with None
df = df.where(pd.notnull(df), None)

records = df.to_dict(orient="records")

# -----------------------------------------
# 4. Connect to MongoDB
# -----------------------------------------

client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=10000
)

client.admin.command("ping")

print("✅ MongoDB connection successful")

db = client[DATABASE_NAME]
collection = db["food_places"]

# -----------------------------------------
# 5. Replace old collection data
# -----------------------------------------

existing_count = collection.count_documents({})

print(f"Existing records in food_places: {existing_count}")

if existing_count > 0:
    collection.delete_many({})
    print("✅ Old food_places records removed")

# -----------------------------------------
# 6. Insert new records
# -----------------------------------------

if records:
    result = collection.insert_many(records)

    print(f"✅ Inserted {len(result.inserted_ids)} records")
else:
    print("❌ No records found to insert")

# -----------------------------------------
# 7. Verify
# -----------------------------------------

final_count = collection.count_documents({})

print("\n========== IMPORT SUMMARY ==========")
print(f"Database: {DATABASE_NAME}")
print("Collection: food_places")
print(f"Final record count: {final_count}")

if final_count == len(df):
    print("\n✅ MongoDB import completed successfully.")
else:
    print("\n⚠️ Record count does not match CSV.")

client.close()