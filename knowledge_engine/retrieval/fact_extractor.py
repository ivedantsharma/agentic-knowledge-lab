import re


def extract_fact(
    text: str,
    pattern: str,
) -> str | None:
    """Extract the first capture group from text using a regex pattern."""
    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    )

    if match is None:
        return None

    if match.lastindex is None:
        raise ValueError(
            "extraction pattern must contain a capture group"
        )

    return match.group(1).strip()
