import stripe
from database.core.config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

try:
    account = stripe.Account.retrieve()
    print("BACKEND ACCOUNT ID:", account.id)
except Exception as e:
    print("ERROR:", e)
