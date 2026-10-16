import pytest

from knowledgebench.metrics.retrieval import precision_at_k, recall_at_k, reciprocal_rank


def test_recall_at_k() -> None:
    retrieved = ["doc_a", "doc_x", "doc_b", "doc_y", "doc_c"]
    relevant = {"doc_a", "doc_b", "doc_c", "doc_d"}

    assert recall_at_k(retrieved, relevant, 5) == pytest.approx(0.75)


def test_precision_at_k() -> None:
    retrieved = ["doc_a", "doc_x", "doc_b", "doc_y", "doc_c"]
    relevant = {"doc_a", "doc_b", "doc_c", "doc_d"}

    assert precision_at_k(retrieved, relevant, 5) == pytest.approx(0.60)


def test_reciprocal_rank_rank_one() -> None:
    retrieved = ["doc_a", "doc_x", "doc_b"]
    relevant = {"doc_a", "doc_b"}

    assert reciprocal_rank(retrieved, relevant) == pytest.approx(1.0)


def test_reciprocal_rank_rank_four() -> None:
    retrieved = ["doc_x", "doc_y", "doc_z", "doc_a"]
    relevant = {"doc_a"}

    assert reciprocal_rank(retrieved, relevant) == pytest.approx(0.25)


def test_reciprocal_rank_no_relevant_result() -> None:
    retrieved = ["doc_x", "doc_y"]
    relevant = {"doc_a"}

    assert reciprocal_rank(retrieved, relevant) == pytest.approx(0.0)

def test_precision_at_k_when_fewer_than_k_results_exist() -> None:
    retrieved = ["doc_a", "doc_b"]
    relevant = {"doc_a", "doc_b"}

    assert precision_at_k(retrieved, relevant, 5) == pytest.approx(1.0)

def test_metrics_with_zero_k() -> None:
    retrieved = ["doc_a"]
    relevant = {"doc_a"}

    assert recall_at_k(retrieved, relevant, 0) == pytest.approx(0.0)
    assert precision_at_k(retrieved, relevant, 0) == pytest.approx(0.0)