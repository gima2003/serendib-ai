import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

APP_NAME = os.getenv("APP_NAME", "Serendib AI")
APP_ENV = os.getenv("APP_ENV", "development")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-that-should-be-changed")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))