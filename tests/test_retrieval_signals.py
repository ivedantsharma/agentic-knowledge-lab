from knowledge_engine.routing.retrieval_signals import (
    build_retrieval_confidence_signals,
)


def test_builds_score_margin_and_overlap_signals() -> None:
    signals = build_retrieval_confidence_signals(
        bm25_ranked=[
            ("a", 4.0),
            ("b", 3.0),
            ("c", 0.0),
        ],
        dense_ranked=[
            ("a", 0.8),
            ("c", 0.7),
            ("d", 0.6),
        ],
    )

    assert signals.bm25_margin == 1.0
    assert signals.bm25_nonzero_count == 2
    assert signals.dense_margin == 0.1
    assert signals.top1_agreement is True
    assert signals.top3_overlap_count == 2
    assert signals.top3_jaccard == 0.5


def test_handles_empty_rankings() -> None:
    signals = build_retrieval_confidence_signals(
        bm25_ranked=[],
        dense_ranked=[],
    )

    assert signals.bm25_margin == 0.0
    assert signals.dense_margin == 0.0
    assert signals.top1_agreement is False
    assert signals.top3_jaccard == 0.0
