import stripe

session_dict = {
  "id": "cs_test_a1",
  "object": "checkout.session",
  "client_reference_id": "6ab355e2ca0c418d3f2f03f7",
  "metadata": {
    "user_id": "6ab355e2ca0c418d3f2f03f7"
  },
  "mode": "subscription",
  "subscription": "sub_1MowQVLkdIwHu7ixVnN8"
}

session = stripe.stripe_object.StripeObject.construct_from(session_dict, "sk_test_123")

user_id = session.get("client_reference_id") or session.get("metadata", {}).get("user_id")
print("Extracted user_id:", user_id)
subscription_id = session.get("subscription")
print("Extracted subscription_id:", subscription_id)
