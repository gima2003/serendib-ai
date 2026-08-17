import os
import re
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient

from services.food_agent.ranking_service import (
    calculate_retrieval_score,
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL was not found in .env")

if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME was not found in .env")


client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=10000
)

db = client[DATABASE_NAME]


food_places_collection = db["food_places"]
food_items_collection = db["food_items"]
food_place_dishes_collection = db["food_place_dishes"]
social_recommendations_collection = db["social_recommendations"]
city_food_profiles_collection = db["city_food_profiles"]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize_text(value) -> str:
    """
    Convert any value to lowercase text safely.
    """

    if value is None:
        return ""

    return str(value).strip().lower()


def contains_keyword(value, keyword) -> bool:
    """
    Case-insensitive keyword matching.
    """

    if not keyword:
        return True

    value_text = normalize_text(value)
    keyword_text = normalize_text(keyword)

    return keyword_text in value_text


def safe_rating(value) -> float:
    """
    Convert rating to a number safely.
    Invalid/missing ratings become 0.
    """

    try:
        rating = float(value)

        if 0 <= rating <= 5:
            return rating

    except (TypeError, ValueError):
        pass

    return 0.0


# =========================================================
# BUDGET MATCHING
# =========================================================

def budget_matches(
    price_value,
    requested_budget: Optional[str]
) -> bool:
    """
    Flexible budget matching.

    Dataset values may look like:
    - Budget signal
    - Rs 1,000–2,000
    - Rs 2,000–3,000
    - Mid
    - Not listed
    """

    if not requested_budget:
        return True

    price = normalize_text(price_value)
    budget = normalize_text(requested_budget)

    if budget in [
        "cheap",
        "budget",
        "low",
        "affordable",
    ]:
        budget_words = [
            "budget",
            "cheap",
            "low",
            "affordable",
            "1,000",
            "1000",
        ]

        return any(
            word in price
            for word in budget_words
        )

    if budget in [
        "mid",
        "medium",
        "moderate",
    ]:
        mid_words = [
            "mid",
            "medium",
            "2,000",
            "2000",
            "3,000",
            "3000",
        ]

        return any(
            word in price
            for word in mid_words
        )

    if budget in [
        "high",
        "premium",
        "expensive",
        "luxury",
    ]:
        high_words = [
            "high",
            "premium",
            "expensive",
            "luxury",
            "4,000",
            "4000",
            "5,000",
            "5000",
        ]

        return any(
            word in price
            for word in high_words
        )

    # Unknown term:
    # do not reject the place automatically.
    return True


# =========================================================
# DIETARY MATCHING
# =========================================================

def dietary_matches(
    dietary_value,
    requested_dietary: Optional[str]
) -> bool:
    """
    Check whether restaurant dietary information
    matches the user's preference.
    """

    if not requested_dietary:
        return True

    dietary_text = normalize_text(dietary_value)
    requested = normalize_text(requested_dietary)

    if requested == "vegetarian":
        return (
            "vegetarian" in dietary_text
            or "veggie" in dietary_text
            or "plant" in dietary_text
        )

    if requested == "vegan":
        return (
            "vegan" in dietary_text
            or "plant-based" in dietary_text
            or "plant based" in dietary_text
        )

    return requested in dietary_text


# =========================================================
# GET DISHES FOR A RESTAURANT
# =========================================================

def get_dishes_for_place(place_id: str):
    """
    Use food_place_dishes as the bridge between
    restaurants and food_items.
    """

    relationships = list(
        food_place_dishes_collection.find(
            {"place_id": place_id},
            {
                "_id": 0,
                "food_id": 1,
                "dish_match_type": 1,
                "evidence_strength": 1,
            }
        )
    )

    if not relationships:
        return []

    food_ids = [
        relationship["food_id"]
        for relationship in relationships
        if relationship.get("food_id")
    ]

    if not food_ids:
        return []

    food_items = list(
        food_items_collection.find(
            {
                "food_id": {
                    "$in": food_ids
                }
            },
            {
                "_id": 0,
                "food_id": 1,
                "food_name": 1,
                "category": 1,
                "meal_type": 1,
                "typical_spice_level": 1,
                "vegetarian_possible": 1,
                "vegan_possible": 1,
                "description": 1,
                "recommendation_tags": 1,
            }
        )
    )

    return food_items


# =========================================================
# GET SOCIAL / REVIEW SIGNALS
# =========================================================

def get_social_signals(
    place_id: str,
    limit: int = 3
):
    """
    Retrieve community/social evidence associated
    with a restaurant.

    Social evidence is supporting evidence only.
    """

    signals = list(
        social_recommendations_collection.find(
            {"place_id": place_id},
            {
                "_id": 0,
                "signal_id": 1,
                "platform": 1,
                "signal_polarity": 1,
                "signal_type": 1,
                "structured_summary": 1,
                "local_vs_tourist_signal": 1,
                "confidence": 1,
                "source_url": 1,
            }
        ).limit(limit)
    )

    return signals


# =========================================================
# BASIC CITY RETRIEVAL
# =========================================================

def find_places_by_city(
    city: str,
    limit: int = 10
):
    """
    Retrieve top-rated food places for a city.
    """

    city_pattern = (
        "^"
        + re.escape(city.strip())
        + "$"
    )

    query = {
        "city": {
            "$regex": city_pattern,
            "$options": "i",
        }
    }

    projection = {
        "_id": 0,
        "place_id": 1,
        "place_name": 1,
        "city": 1,
        "area": 1,
        "address": 1,
        "place_type": 1,
        "cuisine_focus": 1,
        "local_food_strength": 1,
        "dietary_strength": 1,
        "price_band_lkr": 1,
        "rating": 1,
        "review_count": 1,
        "opening_hours": 1,
        "phone": 1,
        "signature_or_recommended_dishes": 1,
        "best_for": 1,
        "source_type": 1,
        "source_url": 1,
        "confidence": 1,
    }

    results = list(
        food_places_collection
        .find(
            query,
            projection
        )
        .sort("rating", -1)
        .limit(limit)
    )

    return results


# =========================================================
# ADVANCED FOOD PLACE RETRIEVAL
# =========================================================

def find_food_places(
    city: str,
    budget: Optional[str] = None,
    dietary: Optional[str] = None,
    cuisine: Optional[str] = None,
    min_rating: Optional[float] = None,
    prefer_local: bool = False,
    limit: int = 10,
):
    """
    Main Food Agent restaurant retrieval function.
    """

    # -----------------------------------------------------
    # STEP 1
    # Retrieve city candidates
    # -----------------------------------------------------

    candidates = find_places_by_city(
        city=city,
        limit=100
    )

    ranked_results = []

    # -----------------------------------------------------
    # STEP 2
    # Filter candidates
    # -----------------------------------------------------

    for place in candidates:

        rating = safe_rating(
            place.get("rating")
        )

        # Minimum rating
        if (
            min_rating is not None
            and rating < min_rating
        ):
            continue

        # Budget match
        budget_match = budget_matches(
            place.get("price_band_lkr"),
            budget
        )

        if budget and not budget_match:
            continue

        # Dietary match
        dietary_match = dietary_matches(
            place.get("dietary_strength"),
            dietary
        )

        if dietary and not dietary_match:
            continue

        # Cuisine match
        cuisine_match = contains_keyword(
            place.get("cuisine_focus"),
            cuisine
        )

        if cuisine and not cuisine_match:
            continue

        # -------------------------------------------------
        # STEP 3
        # Ranking service
        # -------------------------------------------------

        ranking = calculate_retrieval_score(
            place=place,
            budget_match=bool(
                budget and budget_match
            ),
            dietary_match=bool(
                dietary and dietary_match
            ),
            cuisine_match=bool(
                cuisine and cuisine_match
            ),
            prefer_local=prefer_local,
        )

        score = ranking["score"]
        reasons = ranking["reasons"]

        # -------------------------------------------------
        # STEP 4
        # Enrich result
        # -------------------------------------------------

        place_id = place.get("place_id")

        dishes = get_dishes_for_place(
            place_id
        )

        social_signals = get_social_signals(
            place_id,
            limit=3
        )

        # -------------------------------------------------
        # STEP 5
        # Frontend-friendly result
        # -------------------------------------------------

        result = {
            "place_id": place_id,

            "place_name": place.get(
                "place_name"
            ),

            "city": place.get(
                "city"
            ),

            "area": place.get(
                "area"
            ),

            "address": place.get(
                "address"
            ),

            "place_type": place.get(
                "place_type"
            ),

            "cuisine_focus": place.get(
                "cuisine_focus"
            ),

            "local_food_strength": place.get(
                "local_food_strength"
            ),

            "dietary_strength": place.get(
                "dietary_strength"
            ),

            "price_band_lkr": place.get(
                "price_band_lkr"
            ),

            "rating": rating,

            "review_count": place.get(
                "review_count"
            ),

            "opening_hours": place.get(
                "opening_hours"
            ),

            "phone": place.get(
                "phone"
            ),

            "signature_dishes": place.get(
                "signature_or_recommended_dishes"
            ),

            "best_for": place.get(
                "best_for"
            ),

            # Related dishes
            "dishes": dishes,

            # Community evidence
            "social_signals": social_signals,

            # Ranking result
            "retrieval_score": score,

            "match_reasons": reasons,

            # Provenance
            "source": {
                "source_type": place.get(
                    "source_type"
                ),

                "source_url": place.get(
                    "source_url"
                ),

                "confidence": place.get(
                    "confidence"
                ),
            },

            # Map support
            "map_query": (
                f"{place.get('place_name', '')}, "
                f"{place.get('address', '')}"
            ).strip(", "),

            # Photos will be enriched later
            "photo_url": None,
        }

        ranked_results.append(
            result
        )

    # -----------------------------------------------------
    # STEP 6
    # Sort highest score first
    # -----------------------------------------------------

    ranked_results.sort(
        key=lambda item: item[
            "retrieval_score"
        ],
        reverse=True
    )

    # -----------------------------------------------------
    # STEP 7
    # Return top results
    # -----------------------------------------------------

    return ranked_results[:limit]