import re


def normalize_text(value):

    if value is None:
        return ""

    value = str(value).lower().strip()

    value = value.replace(
        "&",
        " and "
    )

    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()