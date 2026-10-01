from datetime import datetime

from database.core.database import db


async def activate_premium_subscription(
    user_id: str,
    subscription_id: str
):

    print("========== PREMIUM ACTIVATION ==========")
    print("USER ID:", user_id)

    result = await db.subscriptions.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "plan": "premium",
                "status": "active",
                "stripe_subscription_id": subscription_id,
                "limits.ai_prompt_limit": -1,
                "limits.guided_plan_limit": -1,
                "updated_at": datetime.utcnow()
            }
        }
    )
    print("MATCHED:", result.matched_count)
    print("MODIFIED:", result.modified_count)
    print("========================================")

    if result.matched_count == 0:
        raise Exception(
            "Subscription not found"
        )

    return True