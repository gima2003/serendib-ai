def has_usage_remaining(
    used: int,
    limit: int
) -> bool:
    """
    Checks whether user still has remaining usage.

    limit:
        -1  -> unlimited
        >0  -> limited usage
    """

    # Premium users
    # -1 means unlimited
    if limit == -1:
        return True

    return used < limit

