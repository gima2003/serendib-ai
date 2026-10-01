from unittest import result

from fastapi import APIRouter, Depends, HTTPException, Request

from payments.stripe_service import (
    create_checkout_session
)
from security.auth_security import get_current_user

import stripe

from database.core.config import (
    STRIPE_WEBHOOK_SECRET
)

from services.subscription_activation_service import (
    activate_premium_subscription
)

from payments.stripe_service import (
    create_checkout_session,
    cancel_subscription
)

from datetime import datetime
from database.core.database import db


router = APIRouter(
    prefix="/api/payment",
    tags=["Payment"]
)


@router.post("/create-checkout")
async def create_payment_checkout(
    current_user: dict = Depends(get_current_user)
):

    try:

        checkout_url = create_checkout_session(
            user_id=str(current_user["_id"]),
            user_email=current_user["email"]
        )


        return {
            "checkout_url": checkout_url
        }


    except Exception as e:

        print("STRIPE CHECKOUT ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Unable to create payment session"
        )

@router.post("/webhook")
async def stripe_webhook(
    request: Request
):

    print("\n🔥🔥 WEBHOOK RECEIVED 🔥🔥\n")

    payload = await request.body()

    signature = request.headers.get(
        "stripe-signature"
    )


    try:

        event = stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET
        )


    except Exception as e:

        print(
            "WEBHOOK SIGNATURE ERROR:",
            e
        )

        raise HTTPException(
            status_code=400,
            detail="Invalid webhook signature"
        )


    print(
        "STRIPE EVENT:",
        event["type"]
    )


    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]


        print("\n========== STRIPE SESSION DEBUG ==========")
        print(session)
        print("==========================================\n")


        print(
            "MODE:",
            session["mode"]
        )


        if session["mode"] != "subscription":

            print(
                "Ignoring non-subscription checkout"
            )

            return {
                "received": True
            }

        
        user_id = session["metadata"]["user_id"]

        print("USER ID FROM STRIPE METADATA:", user_id)
        print(
            "CALLING ACTIVATION:",
            user_id
        )


        subscription_id = session["subscription"]

        await activate_premium_subscription(
            user_id,
            subscription_id
        )

        print("ACTIVATION FINISHED")

        print(
            "PREMIUM ACTIVATED:",
            user_id
        )

    if event["type"] == "customer.subscription.deleted":

        subscription = event["data"]["object"]

        subscription_id = subscription["id"]

        print("\n========== CANCELLATION DEBUG ==========")
        print("STRIPE SUBSCRIPTION ID:", subscription_id)

        mongo_subscription = await db.subscriptions.find_one(
            {
                "stripe_subscription_id": subscription_id
            }
        )

        print("MONGO MATCH:")
        print(mongo_subscription)

        result = await db.subscriptions.update_one(
            {
                "stripe_subscription_id": subscription_id
            },
            {
                "$set": {
                    "plan": "free",
                    "status": "active",
                    "limits.ai_prompt_limit": 3,
                    "limits.guided_plan_limit": 3,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        print("MATCHED:", result.matched_count)
        print("MODIFIED:", result.modified_count)
        print("========================================\n")


    return {
        "received": True
    }

@router.post("/cancel-subscription")
async def cancel_user_subscription(
    current_user: dict = Depends(get_current_user)
):

    subscription = await db.subscriptions.find_one(
        {
            "user_id": str(current_user["_id"])
        }
    )

    if not subscription.get("stripe_subscription_id"):
        raise HTTPException(
            status_code=400,
            detail="No active subscription found"
        )


    cancel_subscription(
        subscription["stripe_subscription_id"]
    )


    return {
        "message": "Cancellation requested"
    }