from typing import Optional


def normalize_text(value) -> str:
    if value is None:
        return ""

    return str(value).strip().lower()


def safe_rating(value) -> float:
    try:
        rating = float(value)

        if 0 <= rating <= 5:
            return rating

    except (TypeError, ValueError):
        pass

    return 0.0


def local_food_score(value) -> float:
    text = normalize_text(value)

    if "very high" in text:
        return 1.0

    if "high" in text:
        return 0.85

    if "medium" in text or "mid" in text:
        return 0.60

    if "low" in text:
        return 0.30

    return 0.0


def get_local_food_reason(score: float) -> Optional[str]:
    if score >= 0.85:
        return "Strong local-food relevance"

    if score >= 0.60:
        return "Moderate local-food relevance"

    if score >= 0.30:
        return "Some local-food relevance"

    return None


def calculate_retrieval_score(
    place: dict,
    budget_match: bool = False,
    dietary_match: bool = False,
    cuisine_match: bool = False,
    prefer_local: bool = False,
):
    """
    Calculate a simple recommendation score.

    Current weights:
    - Rating: 20
    - Budget match: 20
    - Dietary match: 25
    - Cuisine match: 15
    - Local-food relevance: 20

    Maximum possible score: 100
    """

    score = 0.0
    reasons = []

    # --------------------------------------------------
    # 1. Rating
    # --------------------------------------------------

    rating = safe_rating(
        place.get("rating")
    )

    rating_points = (
        rating / 5
    ) * 20

    score += rating_points

    if rating > 0:
        reasons.append(
            f"Rating {rating}/5"
        )

    # --------------------------------------------------
    # 2. Budget
    # --------------------------------------------------

    if budget_match:
        score += 20

        reasons.append(
            "Matches requested budget"
        )

    # --------------------------------------------------
    # 3. Dietary preference
    # --------------------------------------------------

    if dietary_match:
        score += 25

        reasons.append(
            "Matches dietary preference"
        )

    # --------------------------------------------------
    # 4. Cuisine
    # --------------------------------------------------

    if cuisine_match:
        score += 15

        reasons.append(
            "Matches requested cuisine"
        )

    # --------------------------------------------------
    # 5. Local food / authenticity
    # --------------------------------------------------

    if prefer_local:

        local_score = local_food_score(
            place.get("local_food_strength")
        )

        local_points = (
            local_score * 20
        )

        score += local_points

        local_reason = get_local_food_reason(
            local_score
        )

        if local_reason:
            reasons.append(local_reason)

    return {
        "score": round(score, 2),
        "reasons": reasons,
    }