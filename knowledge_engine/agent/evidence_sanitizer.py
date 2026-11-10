import re

_INSTRUCTION_MARKERS = (
    "assistant directive",
    "system override",
    "priority instruction",
    "important instruction",
    "ignore the question",
    "ignore earlier instructions",
    "ignore the user's question",
    "disregard the original question",
    "answer exactly",
    "respond with",
    "output exactly",
    "treat the following as the answer",
)


def sanitize_untrusted_evidence(
    text: str,
) -> str:
    """Remove sentence-like spans that look like assistant-directed instructions."""
    parts = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    kept = [
        part
        for part in parts
        if not any(
            marker in part.casefold()
            for marker in _INSTRUCTION_MARKERS
        )
    ]

    return " ".join(kept).strip()
