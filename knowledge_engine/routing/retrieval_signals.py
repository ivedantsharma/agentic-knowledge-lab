from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalConfidenceSignals:
    bm25_top1_score: float
    bm25_top2_score: float
    bm25_margin: float
    bm25_nonzero_count: int

    dense_top1_score: float
    dense_top2_score: float
    dense_margin: float

    top1_agreement: bool
    top3_overlap_count: int
    top3_jaccard: float


def _margin(
    ranked: list[tuple[str, float]],
) -> float:
    if len(ranked) < 2:
        return 0.0

    return ranked[0][1] - ranked[1][1]


def build_retrieval_confidence_signals(
    bm25_ranked: list[tuple[str, float]],
    dense_ranked: list[tuple[str, float]],
) -> RetrievalConfidenceSignals:
    bm25_top1_score = (
        bm25_ranked[0][1]
        if bm25_ranked
        else 0.0
    )
    bm25_top2_score = (
        bm25_ranked[1][1]
        if len(bm25_ranked) >= 2
        else 0.0
    )

    dense_top1_score = (
        dense_ranked[0][1]
        if dense_ranked
        else 0.0
    )
    dense_top2_score = (
        dense_ranked[1][1]
        if len(dense_ranked) >= 2
        else 0.0
    )

    bm25_top3 = {
        document_id
        for document_id, _score
        in bm25_ranked[:3]
    }
    dense_top3 = {
        document_id
        for document_id, _score
        in dense_ranked[:3]
    }

    union = bm25_top3 | dense_top3
    overlap = bm25_top3 & dense_top3

    return RetrievalConfidenceSignals(
        bm25_top1_score=bm25_top1_score,
        bm25_top2_score=bm25_top2_score,
        bm25_margin=_margin(bm25_ranked),
        bm25_nonzero_count=sum(
            score > 0.0
            for _document_id, score
            in bm25_ranked
        ),
        dense_top1_score=dense_top1_score,
        dense_top2_score=dense_top2_score,
        dense_margin=_margin(dense_ranked),
        top1_agreement=(
            bool(bm25_ranked)
            and bool(dense_ranked)
            and bm25_ranked[0][0]
            == dense_ranked[0][0]
        ),
        top3_overlap_count=len(overlap),
        top3_jaccard=(
            len(overlap) / len(union)
            if union
            else 0.0
        ),
    )
