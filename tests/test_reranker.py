import pytest

from knowledge_engine.retrieval.reranker import (
    sort_by_reranker_scores,
)


def test_sort_by_reranker_scores() -> None:
    ranked = sort_by_reranker_scores(
        ["a", "b", "c"],
        [0.1, 0.9, 0.4],
    )

    assert ranked == ["b", "c", "a"]


def test_reranker_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        sort_by_reranker_scores(
            ["a", "b"],
            [0.5],
        )
