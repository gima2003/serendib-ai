import stripe
import time
from database.core.config import STRIPE_WEBHOOK_SECRET

payload = b'{"id": "evt_test", "type": "checkout.session.completed", "data": {"object": {"mode": "subscription", "metadata": {"user_id": "test_123"}, "subscription": "sub_test"}}}'
secret = STRIPE_WEBHOOK_SECRET or "whsec_test"
timestamp = int(time.time())
signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
signature = stripe.WebhookSignature._compute_signature(signed_payload, secret)
header = f"t={timestamp},v1={signature}"

try:
    event = stripe.Webhook.construct_event(payload, header, secret)
    session = event["data"]["object"]
    session_dict = session.to_dict()
    user_id = session_dict.get("client_reference_id") or session_dict.get("metadata", {}).get("user_id")
    print("SUCCESS user_id:", user_id)
except Exception as e:
    print("ERROR:", e)
