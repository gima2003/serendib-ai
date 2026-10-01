import stripe

from database.core.config import STRIPE_SECRET_KEY


stripe.api_key = STRIPE_SECRET_KEY



def create_checkout_session(
    user_id: str,
    user_email: str
):
    print("\n========== STRIPE ACCOUNT DEBUG ==========")

    account = stripe.Account.retrieve()

    print("BACKEND STRIPE ACCOUNT:")
    print(account["id"])

    print("==========================================\n")

    session = stripe.checkout.Session.create(

        

        mode="subscription",

        customer_email=user_email,

        client_reference_id=user_id,

        metadata={
            "user_id": user_id
        },

        line_items=[
            {
                "price_data": {

                    "currency": "usd",

                    "product_data": {
                        "name": "Serendib AI Premium"
                    },

                    "unit_amount": 999,

                    "recurring": {
                        "interval": "month"
                    }
                },

                "quantity": 1
            }
        ],

        success_url=
        "http://localhost:5173/dashboard?payment=success",

        cancel_url=
        "http://localhost:5173/subscription"
    )

    print("CHECKOUT SESSION ACCOUNT:")
    print(session.account if hasattr(session, "account") else "NO ACCOUNT FIELD")
    print("\n========== STRIPE CHECKOUT DEBUG ==========")

    print("USER ID:", user_id)

    print("EMAIL:", user_email)

    print("MODE:", session.mode)

    print("URL:", session.url)

    print("METADATA:", session.metadata)

    print("===========================================\n")

    print(
        "STRIPE ACCOUNT:",
        stripe.Account.retrieve()["id"]
    )


    return session.url

def cancel_subscription(subscription_id):

    print("SUB ID:", subscription_id)

    subscription = stripe.Subscription.retrieve(
        subscription_id
    )

    print("CURRENT STATUS:", subscription.status)


    if subscription.status == "canceled":
        return subscription


    return stripe.Subscription.delete(
        subscription_id
    )