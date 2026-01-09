from fastapi import APIRouter, HTTPException, Depends
from uuid import uuid4
from datetime import datetime
from app.models.user import UserCreate
from app.db.mongo import users_collection
from app.core.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(data: UserCreate):
    existing = await users_collection.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = {
        "id": str(uuid4()),
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "created_at": datetime.utcnow(),
    }

    await users_collection.insert_one(user)
    return {"message": "User created successfully"}

@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return current_user

@router.post("/login")
async def login(data: UserCreate):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["id"]})
    return {"access_token": token, "token_type": "bearer"}
