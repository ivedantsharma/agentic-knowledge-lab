import pytest

from knowledgebench.evaluation.retrieval_evaluator import (
    mean_precision_at_k,
    mean_recall_at_k,
    mean_reciprocal_rank,
)


def test_mean_recall_at_k() -> None:
    retrieved = {
        "q1": ["a", "x", "b"],
        "q2": ["z", "c"],
    }
    relevant = {
        "q1": {"a", "b"},
        "q2": {"c", "d"},
    }

    # q1 recall@3 = 2/2 = 1.0
    # q2 recall@3 = 1/2 = 0.5
    # mean = 0.75
    assert mean_recall_at_k(retrieved, relevant, 3) == pytest.approx(0.75)


def test_mean_precision_at_k() -> None:
    retrieved = {
        "q1": ["a", "x", "b"],
        "q2": ["z", "c"],
    }
    relevant = {
        "q1": {"a", "b"},
        "q2": {"c", "d"},
    }

    # q1 precision@3 = 2/3
    # q2 precision@3 = 1/2 because only 2 docs were retrieved
    expected = ((2 / 3) + (1 / 2)) / 2
    assert mean_precision_at_k(retrieved, relevant, 3) == pytest.approx(expected)


def test_mean_reciprocal_rank() -> None:
    retrieved = {
        "q1": ["a", "x", "b"],
        "q2": ["z", "c"],
    }
    relevant = {
        "q1": {"a", "b"},
        "q2": {"c", "d"},
    }

    # q1 RR = 1.0
    # q2 RR = 1/2
    # MRR = 0.75
    assert mean_reciprocal_rank(retrieved, relevant) == pytest.approx(0.75)


def test_missing_retrieval_output_counts_as_failure() -> None:
    retrieved = {
        "q1": ["a"],
    }
    relevant = {
        "q1": {"a"},
        "q2": {"b"},
    }

    assert mean_recall_at_k(retrieved, relevant, 1) == pytest.approx(0.5)
    assert mean_reciprocal_rank(retrieved, relevant) == pytest.approx(0.5)


def test_empty_benchmark_returns_zero() -> None:
    assert mean_recall_at_k({}, {}, 5) == pytest.approx(0.0)
    assert mean_precision_at_k({}, {}, 5) == pytest.approx(0.0)
    assert mean_reciprocal_rank({}, {}) == pytest.approx(0.0)
