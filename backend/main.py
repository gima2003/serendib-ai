from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pymongo

from database.core.database import db

# Routers
from routes.auth_routes import router as auth_router
from routes.destination_routes import router as destination_router
from routes.profile_route import router as profile_router
from routes.planner_routes import router as planner_router
from routes.food_routes import router as food_router



# ==================================================
# Application Lifespan
# ==================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n========================================")

    try:

        # Test MongoDB connection
        await db.command("ping")


        # Create unique email index
        await db.users.create_index(
            [
                ("email", pymongo.ASCENDING)
            ],
            unique=True
        )


        print("🚀 Serendib AI Backend Running")
        print("✅ MongoDB Atlas Connected Successfully")
        print("🌐 API: http://127.0.0.1:8000")
        print("📚 Docs: http://127.0.0.1:8000/docs")


    except Exception as e:

        print("❌ MongoDB Atlas Connection Failed")
        print(f"Error: {e}")


    print("========================================\n")


    yield


    # Shutdown logic (optional)

    print("\n🛑 Serendib AI Backend Shutdown\n")



# ==================================================
# FastAPI Application
# ==================================================

app = FastAPI(

    title="Serendib AI API",

    version="1.0.0",

    lifespan=lifespan

)



# ==================================================
# CORS Configuration
# ==================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



# ==================================================
# API Routers
# ==================================================

app.include_router(
    auth_router
)


app.include_router(
    destination_router
)


app.include_router(
    profile_router
)


app.include_router(
    planner_router
)


app.include_router(
    food_router
)



# ==================================================
# Health Check APIs
# ==================================================

@app.get("/")
async def root():

    return {

        "status": "success",

        "message":
            "Serendib AI Backend Running",

        "database":
            "MongoDB Atlas"

    }



@app.get("/test-db")
async def test_database():

    try:

        await db.command("ping")


        return {

            "status": "success",

            "message":
                "MongoDB Atlas Connected Successfully"

        }


    except Exception as e:

        return {

            "status": "error",

            "message":
                "MongoDB Atlas Connection Failed",

            "error":
                str(e)

        }