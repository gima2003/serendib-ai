from fastapi import APIRouter, Depends, HTTPException

from security.auth_security import get_current_user

from services.subscription_service import (
    get_or_create_subscription,
    update_subscription_plan
)
from services.subscription_guard import (
    check_ai_prompt_access,
    check_guided_plan_access,
    increment_ai_prompt_usage
)



router = APIRouter(
    prefix="/api/subscription",
    tags=["Subscription"]
)


@router.get("/current")
async def get_current_subscription(
    current_user: dict = Depends(get_current_user)
):
    print("🔥🔥 SUBSCRIPTION CURRENT ROUTE HIT 🔥🔥")
    try:
        print("\n========== SUBSCRIPTION DEBUG ==========")

        print("CURRENT USER:")
        print(current_user)

        user_id = str(current_user["_id"])

        print("USER ID:")
        print(user_id)


        subscription = await get_or_create_subscription(
            user_id
        )

        print("SUBSCRIPTION:")
        print(subscription)

        print("========================================\n")


        return {
            "subscription": subscription
        }


    except Exception as e:

        print("\n========== SUBSCRIPTION ERROR ==========")
        print(type(e))
        print(str(e))
        print("========================================\n")

        raise e

@router.post("/select")
async def select_subscription_plan(
    plan: str,
    current_user: dict = Depends(get_current_user)
):

    print("\n========== SELECT SUBSCRIPTION DEBUG ==========")

    print("PLAN:")
    print(plan)

    user_id = str(current_user["_id"])

    print("USER ID:")
    print(user_id)


    subscription = await update_subscription_plan(
        user_id=user_id,
        new_plan=plan
    )

    print("UPDATED SUBSCRIPTION:")
    print(subscription)

    print("===============================================\n")


    return {
        "message": "Subscription updated successfully",
        "subscription": subscription
    }



@router.post("/test-ai-usage")
async def test_ai_usage(
    current_user: dict = Depends(get_current_user)
):

    user_id = str(current_user["_id"])


    await check_ai_prompt_access(
        user_id
    )


    await increment_ai_prompt_usage(
        user_id
    )


    return {
        "message": "AI usage counted"
    }

@router.get("/check-guided-plan")
async def check_guided_plan(
    current_user: dict = Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    try:

        await check_guided_plan_access(
            user_id
        )

        return {
            "allowed": True
        }


    except HTTPException as error:

        raise error

