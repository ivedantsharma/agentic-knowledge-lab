import pytest

from knowledge_engine.retrieval.fact_extractor import (
    extract_fact,
)


def test_extract_fact_returns_first_capture_group() -> None:
    text = (
        "Atlas is operated by the Platform Reliability team."
    )

    fact = extract_fact(
        text,
        r"operated by the (.+?) team",
    )

    assert fact == "Platform Reliability"


def test_extract_fact_returns_none_when_pattern_does_not_match() -> None:
    assert extract_fact(
        "No relation is present.",
        r"maintains the (.+?) storage system",
    ) is None


def test_extract_fact_requires_capture_group() -> None:
    with pytest.raises(ValueError):
        extract_fact(
            "Atlas is operated by Platform Reliability.",
            r"operated by Platform Reliability",
        )
