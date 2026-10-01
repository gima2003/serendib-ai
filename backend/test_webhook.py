import asyncio
from database.core.database import db
from services.subscription_activation_service import activate_premium_subscription
import sys

async def test():
    user = await db.users.find_one()
    if not user:
        print("No user")
        return
    user_id = str(user["_id"])
    print("User ID:", user_id)
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        print("No sub")
        return
    print("Before:", sub["plan"])
    await activate_premium_subscription(user_id, "sub_123")
    sub = await db.subscriptions.find_one({"user_id": user_id})
    print("After:", sub["plan"])

asyncio.run(test())
