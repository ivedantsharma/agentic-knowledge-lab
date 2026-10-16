def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Return Recall@K for one query."""
    # TODO: implement this yourself.
    raise NotImplementedError


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Return Precision@K for one query."""
    # TODO: implement this yourself.
    raise NotImplementedError


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float:
    """Return reciprocal rank of the first relevant result."""
    # TODO: implement this yourself.
    raise NotImplementedError
