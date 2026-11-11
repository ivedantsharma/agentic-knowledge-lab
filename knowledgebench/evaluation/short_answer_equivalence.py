import re

_NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
}


def canonicalize_short_answer(
    value: str | None,
) -> str:
    if value is None:
        return ""

    normalized = " ".join(
        value.casefold().split()
    )

    tokens = [
        _NUMBER_WORDS.get(token, token)
        for token in normalized.split()
    ]
    normalized = " ".join(tokens)

    normalized = normalized.removeprefix("every ")

    return normalized


def short_answers_equivalent(
    candidate: str | None,
    expected: str | None,
) -> bool:
    candidate_value = canonicalize_short_answer(
        candidate
    )
    expected_value = canonicalize_short_answer(
        expected
    )

    if candidate_value == expected_value:
        return True

    candidate_number = re.fullmatch(
        r"\d+",
        candidate_value,
    )
    expected_count = re.fullmatch(
        r"(\d+) times",
        expected_value,
    )

    return bool(
        candidate_number
        and expected_count
        and candidate_number.group(0)
        == expected_count.group(1)
    )
