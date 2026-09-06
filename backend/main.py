from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from database.core.database import db
from routes.auth_routes import router as auth_router
from routes.destination_routes import router as destination_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs when backend starts
    try:
        await db.command("ping")
        # Ensure unique index on user email
        await db.users.create_index([("email", pymongo.ASCENDING)], unique=True)
        print("\n========================================")
        print("🚀 Serendib AI Backend Running")
        print("✅ MongoDB Atlas Connected Successfully")
        print("🌐 API: http://127.0.0.1:8000")
        print("📚 Docs: http://127.0.0.1:8000/docs")
        print("========================================\n")

    except Exception as e:
        print("\n========================================")
        print("❌ MongoDB Atlas Connection Failed")
        print(f"Error: {e}")
        print("========================================\n")

    yield


app = FastAPI(
    title="Serendib AI API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(destination_router)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Serendib AI Backend Running",
        "database": "MongoDB Atlas"
    }


@app.get("/test-db")
async def test_database():
    try:
        await db.command("ping")

        return {
            "status": "success",
            "message": "MongoDB Atlas Connected Successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "MongoDB Atlas Connection Failed",
            "error": str(e)
        }