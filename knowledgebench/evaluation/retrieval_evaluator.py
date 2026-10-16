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
    recalls = [
        recall_at_k(retrieved_by_query.get(query_id, []), relevant, k)
        for query_id, relevant in relevant_by_query.items()
    ]
    return sum(recalls) / len(recalls) if recalls else 0.0


def mean_precision_at_k(
    retrieved_by_query: dict[str, list[str]],
    relevant_by_query: dict[str, set[str]],
    k: int,
) -> float:
    """Return mean Precision@K across all benchmark queries."""
    precisions = [
        precision_at_k(retrieved_by_query.get(query_id, []), relevant, k)
        for query_id, relevant in relevant_by_query.items()
    ]
    return sum(precisions) / len(precisions) if precisions else 0.0


def mean_reciprocal_rank(
    retrieved_by_query: dict[str, list[str]],
    relevant_by_query: dict[str, set[str]],
) -> float:
    """Return Mean Reciprocal Rank across all benchmark queries."""
    rrs = [
        reciprocal_rank(retrieved_by_query.get(query_id, []), relevant)
        for query_id, relevant in relevant_by_query.items()
    ]
    return sum(rrs) / len(rrs) if rrs else 0.0
