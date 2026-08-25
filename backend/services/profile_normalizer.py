from models.traveller_profile import TravellerProfile

DIETARY_NORMALIZATION = {
    "veg": "vegetarian",
    "vegeterian": "vegetarian",
    "vegitarian": "vegetarian",

    "veggie": "vegetarian",

    "vegan diet": "vegan",

    "halal food": "halal",

    "gluten free": "gluten_free",
    "gluten-free": "gluten_free",
}


CURRENCY_NORMALIZATION = {
    "usd": "USD",
    "us dollar": "USD",
    "us dollars": "USD",
    "dollar": "USD",
    "dollars": "USD",

    "lkr": "LKR",
    "sri lankan rupee": "LKR",
    "sri lankan rupees": "LKR",
    "rupees": "LKR",

    "eur": "EUR",
    "euro": "EUR",
    "euros": "EUR",

    "gbp": "GBP",
    "pound": "GBP",
    "pounds": "GBP",
}

def normalize_dietary_requirement(value: str) -> str:
    cleaned_value = value.strip().lower()

    return DIETARY_NORMALIZATION.get(cleaned_value, cleaned_value)



def normalize_currency(value: str) -> str:
    cleaned_value = value.strip().lower()

    return CURRENCY_NORMALIZATION.get(cleaned_value, value.strip().upper())


def normalize_traveller_profile(profile: TravellerProfile) -> TravellerProfile:
    if profile.budget.currency is not None:
        profile.budget.currency = normalize_currency(
            profile.budget.currency
        )

    profile.dietary_requirements = [
        normalize_dietary_requirement(requirement)
        for requirement in profile.dietary_requirements
    ]

    return profile