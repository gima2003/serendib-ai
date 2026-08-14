import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load variables from .env
load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")
database_name = os.getenv("MONGODB_DB_NAME")

try:
    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=5000
    )

    # Ask MongoDB server to respond
    client.admin.command("ping")

    print("✅ MongoDB connection successful!")
    print(f"✅ Database selected: {database_name}")

except Exception as e:
    print("❌ MongoDB connection failed!")
    print(e)