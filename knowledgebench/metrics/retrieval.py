def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Return Recall@K for one query."""
    if k <= 0 or not relevant_ids:
        return 0.0

    top_k = retrieved_ids[:k]
    relevant_retrieved = len(set(top_k) & relevant_ids)

    return relevant_retrieved / len(relevant_ids)

def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Return Precision@K for one query."""
    if k <= 0:
        return 0.0

    top_k = retrieved_ids[:k]

    if not top_k:
        return 0.0

    relevant_retrieved = len(set(top_k) & relevant_ids)
    
    return relevant_retrieved / len(top_k)

def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float:
    """Return reciprocal rank of the first relevant result."""
    if not relevant_ids:
        return 0.0

    for rank, document_id in enumerate(retrieved_ids, start=1):
        if document_id in relevant_ids:
            return 1.0 / rank

    return 0.0