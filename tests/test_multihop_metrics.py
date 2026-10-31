import pytest

from knowledgebench.metrics.multihop import (
    exact_chain_match,
    hop_accuracy,
)


def test_hop_accuracy() -> None:
    assert hop_accuracy(
        ["a", "x", "c"],
        ["a", "b", "c"],
    ) == pytest.approx(2 / 3)


def test_exact_chain_match() -> None:
    assert exact_chain_match(
        ["a", "b"],
        ["a", "b"],
    ) == 1.0

    assert exact_chain_match(
        ["a", "x"],
        ["a", "b"],
    ) == 0.0


def test_hop_accuracy_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError):
        hop_accuracy(
            ["a"],
            ["a", "b"],
        )
