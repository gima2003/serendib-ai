import re


def normalize_text(text):
    """
    Normalize text for matching.

    Example:
    "  Beach  " -> "beach"
    "Photography " -> "photography"
    """

    if text is None:
        return ""


    text = str(text)


    # lowercase
    text = text.lower()


    # remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )


    # remove leading/trailing spaces
    text = text.strip()


    return text