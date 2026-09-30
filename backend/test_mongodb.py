import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load variables from .env
load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")
database_name = os.getenv("DATABASE_NAME")

try:
    client = MongoClient(
        mongodb_url,
        serverSelectionTimeoutMS=5000
    )

    # Ask MongoDB Atlas server to respond
    client.admin.command("ping")

    db = client[database_name]

    print("✅ MongoDB connection successful!")
    print(f"✅ Database selected: {database_name}")

except Exception as e:
    print("❌ MongoDB connection failed!")
    print(e)