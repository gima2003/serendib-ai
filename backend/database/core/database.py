from pymongo import AsyncMongoClient
from database.core.config import MONGODB_URL, DATABASE_NAME

client = AsyncMongoClient(MONGODB_URL)

db = client[DATABASE_NAME]