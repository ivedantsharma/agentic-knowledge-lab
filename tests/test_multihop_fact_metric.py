import pytest

from knowledgebench.metrics.multihop import (
    fact_accuracy,
)


def test_fact_accuracy() -> None:
    assert fact_accuracy(
        ["Platform Reliability", "Borealis", None],
        ["Platform Reliability", "Borealis", "every six hours"],
    ) == pytest.approx(2 / 3)


def test_fact_accuracy_is_case_insensitive() -> None:
    assert fact_accuracy(
        ["borealis"],
        ["Borealis"],
    ) == 1.0


def test_fact_accuracy_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError):
        fact_accuracy(
            ["Borealis"],
            ["Borealis", "six hours"],
        )
