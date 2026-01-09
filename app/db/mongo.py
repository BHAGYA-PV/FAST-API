from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["fastapi_db"]
users_collection = db["users"]
books_collection = db["books"]