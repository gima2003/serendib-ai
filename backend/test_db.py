import asyncio
from database.core.database import db

async def check():
    sub = await db.subscriptions.find_one()
    if sub:
        print("Type of user_id in DB:", type(sub["user_id"]))
        print("Type of _id in DB:", type(sub["_id"]))

asyncio.run(check())
