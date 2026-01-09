import asyncio
from app.db.mongo import users_collection

async def test():
    count = await users_collection.count_documents({})
    print("Users in DB:", count)

asyncio.run(test())
