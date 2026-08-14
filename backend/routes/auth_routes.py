from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from database.core.database import db
from models.auth_schema import UserRegister, UserLogin, Token, UserResponse
from security.auth_security import get_password_hash, verify_password, create_access_token, get_current_user
from database.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister) -> Any:
    # Check if email already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Prepare user document
    now = datetime.utcnow()
    user_dict = {
        "full_name": user_data.full_name,
        "email": user_data.email,
        "country_code": user_data.country_code,
        "preferred_currency": user_data.preferred_currency,
        "password_hash": hashed_password,
        "role": "traveler",
        "is_active": True,
        "created_at": now,
        "updated_at": now
    }

    # Insert to MongoDB
    try:
        result = await db.users.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    user_dict["id"] = str(result.inserted_id)
    return user_dict

@router.post("/login", response_model=Any) # Token + User info
async def login(login_data: UserLogin) -> Any:
    # Find user by email
    user = await db.users.find_one({"email": login_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Verify password
    if not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Check if active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Generate JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    # Update last_login
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    user["id"] = str(user["_id"])
    user_response = UserResponse(**user).model_dump()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)) -> Any:
    current_user["id"] = str(current_user["_id"])
    return current_user

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)) -> Any:
    # Basic stateless logout. Frontend will discard token.
    return {"message": "Successfully logged out"}
