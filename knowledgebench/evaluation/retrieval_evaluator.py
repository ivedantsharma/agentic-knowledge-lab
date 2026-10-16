from knowledgebench.metrics.retrieval import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def mean_recall_at_k(
    retrieved_by_query: dict[str, list[str]],
    relevant_by_query: dict[str, set[str]],
    k: int,
) -> float:
    """Return mean Recall@K across all benchmark queries."""
    # TODO: implement this yourself.
    raise NotImplementedError


def mean_precision_at_k(
    retrieved_by_query: dict[str, list[str]],
    relevant_by_query: dict[str, set[str]],
    k: int,
) -> float:
    """Return mean Precision@K across all benchmark queries."""
    # TODO: implement this yourself.
    raise NotImplementedError


def mean_reciprocal_rank(
    retrieved_by_query: dict[str, list[str]],
    relevant_by_query: dict[str, set[str]],
) -> float:
    """Return Mean Reciprocal Rank across all benchmark queries."""
    # TODO: implement this yourself.
    raise NotImplementedError
