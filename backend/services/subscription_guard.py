from datetime import datetime

from fastapi import HTTPException

from database.core.database import db


FREE_PLAN = "free"
PREMIUM_PLAN = "premium"



async def get_user_subscription(user_id: str):

    subscription = await db.subscriptions.find_one(
        {
            "user_id": user_id
        }
    )


    if not subscription:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )


    return subscription



async def check_ai_prompt_access(user_id: str):

    subscription = await get_user_subscription(
        user_id
    )


    # Premium users have unlimited access
    if subscription["plan"] == PREMIUM_PLAN:

        return True



    usage = subscription.get(
        "usage",
        {}
    )


    limits = subscription.get(
        "limits",
        {}
    )


    used = usage.get(
        "ai_prompts_used",
        0
    )


    limit = limits.get(
        "ai_prompt_limit",
        3
    )


    if used >= limit:

        raise HTTPException(
            status_code=403,
            detail={
                "message":
                    "Free AI prompt limit reached. Upgrade to Premium to continue.",
                "feature":
                    "ai_prompt"
            }
        )


    return True



async def check_guided_plan_access(user_id: str):

    subscription = await get_user_subscription(
        user_id
    )


    # Premium unlimited
    if subscription["plan"] == PREMIUM_PLAN:

        return True



    usage = subscription.get(
        "usage",
        {}
    )


    limits = subscription.get(
        "limits",
        {}
    )


    used = usage.get(
        "guided_plans_used",
        0
    )


    limit = limits.get(
        "guided_plan_limit",
        3
    )


    if used >= limit:

        raise HTTPException(
            status_code=403,
            detail={
                "message":
                    "Free guided trip limit reached. Upgrade to Premium to continue.",
                "feature":
                    "guided_plan"
            }
        )


    return True

async def increment_ai_prompt_usage(user_id: str):

    await db.subscriptions.update_one(
        {
            "user_id": user_id
        },
        {
            "$inc": {
                "usage.ai_prompts_used": 1
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )



async def increment_guided_plan_usage(user_id: str):

    await db.subscriptions.update_one(
        {
            "user_id": user_id
        },
        {
            "$inc": {
                "usage.guided_plans_used": 1
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )