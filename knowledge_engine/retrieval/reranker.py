from collections.abc import Sequence


def sort_by_reranker_scores(
    candidate_ids: Sequence[str],
    scores: Sequence[float],
) -> list[str]:
    """Sort candidate IDs by reranker score, highest first."""
    if len(candidate_ids) != len(scores):
        raise ValueError(
            "candidate_ids and scores must have equal length"
        )

    paired = list(zip(candidate_ids, scores))

    paired.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        candidate_id
        for candidate_id, _ in paired
    ]
