from datetime import datetime

from bson import ObjectId

from database.core.database import db
from config.subscription_plans import SUBSCRIPTION_PLANS


async def create_subscription(
    user_id: str,
    plan_name: str = "free"
):
    """
    Create a subscription record for a user.
    """

    if plan_name not in SUBSCRIPTION_PLANS:
        raise ValueError(
            "Invalid subscription plan"
        )


    plan = SUBSCRIPTION_PLANS[plan_name]


    now = datetime.utcnow()


    subscription = {

        "user_id": user_id,

        "plan": plan_name,

        "status": "active",


        "usage": {

            "ai_prompts_used": 0,

            "guided_plans_used": 0

        },


        "limits": {

            "ai_prompt_limit":
                plan["limits"]["ai_prompt_limit"],

            "guided_plan_limit":
                plan["limits"]["guided_plan_limit"]

        },


        "created_at": now,

        "updated_at": now

    }


    result = await db.subscriptions.insert_one(
        subscription
    )


    subscription["_id"] = str(result.inserted_id)


    return subscription



async def get_user_subscription(
    user_id: str
):

    subscription = await db.subscriptions.find_one(
        {
            "user_id": user_id
        }
    )


    if subscription and "_id" in subscription:
        subscription["_id"] = str(
            subscription["_id"]
        )


    return subscription


async def get_or_create_subscription(
    user_id: str
):
    """
    Ensures every user has a subscription.
    """


    subscription = await get_user_subscription(
        user_id
    )


    if subscription:

        if "_id" in subscription:
            subscription["_id"] = str(subscription["_id"])

        return subscription


    return await create_subscription(
        user_id=user_id,
        plan_name="free"
    )



async def update_subscription_plan(
    user_id: str,
    new_plan: str
):

    if new_plan not in SUBSCRIPTION_PLANS:
        raise ValueError(
            "Invalid subscription plan"
        )


    plan = SUBSCRIPTION_PLANS[new_plan]


    await db.subscriptions.update_one(
        {
            "user_id": user_id
        },

        {
            "$set": {

                "plan": new_plan,

                "limits": {

                    "ai_prompt_limit":
                        plan["limits"]["ai_prompt_limit"],

                    "guided_plan_limit":
                        plan["limits"]["guided_plan_limit"]

                },

                "updated_at":
                    datetime.utcnow()

            }
        }
    )


    return await get_user_subscription(
        user_id
    )