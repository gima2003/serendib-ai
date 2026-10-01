import asyncio
import httpx
import time
import stripe
from database.core.config import STRIPE_WEBHOOK_SECRET
from database.core.database import db

async def run_test():
    user = await db.users.find_one({"email": "umarahamed852@gmail.com"})
    if not user:
        print("User not found.")
        return
    user_id = str(user["_id"])
    print("Testing for User ID:", user_id)
    
    payload = f'{{"id": "evt_test", "type": "checkout.session.completed", "data": {{"object": {{"mode": "subscription", "client_reference_id": "{user_id}", "subscription": "sub_test_123"}}}}}}'
    payload_bytes = payload.encode('utf-8')
    
    secret = STRIPE_WEBHOOK_SECRET
    timestamp = int(time.time())
    signed_payload = f"{timestamp}.{payload}"
    signature = stripe.WebhookSignature._compute_signature(signed_payload, secret)
    header = f"t={timestamp},v1={signature}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8000/api/payment/webhook",
                content=payload_bytes,
                headers={"stripe-signature": header, "Content-Type": "application/json"}
            )
            print("Webhook response:", response.status_code, response.text)
        except Exception as e:
            print("Request failed:", e)
        
    sub = await db.subscriptions.find_one({"user_id": user_id})
    print("Subscription Plan after webhook:", sub.get("plan"))

asyncio.run(run_test())
