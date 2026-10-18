from collections import defaultdict


def reciprocal_rank_fusion(
    rankings: list[list[str]],
    top_k: int,
    rrf_k: int = 60,
) -> list[tuple[str, float]]:
    """Fuse multiple ranked document-ID lists using Reciprocal Rank Fusion."""
    if top_k <= 0:
        return []

    scores: dict[str, float] = defaultdict(float)

    for ranking in rankings:
        for rank, document_id in enumerate(ranking, start=1):
            scores[document_id] += 1.0 / (rrf_k + rank)

    fused = sorted(
        scores.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return fused[:top_k]
