from knowledge_engine.retrieval.hybrid import reciprocal_rank_fusion


def test_rrf_rewards_documents_supported_by_multiple_rankings() -> None:
    fused = reciprocal_rank_fusion(
        rankings=[
            ["a", "b", "c"],
            ["b", "d", "a"],
        ],
        top_k=4,
    )

    ranked_ids = [document_id for document_id, _ in fused]

    assert ranked_ids[0] in {"a", "b"}
    assert set(ranked_ids[:2]) == {"a", "b"}


def test_rrf_returns_top_k() -> None:
    fused = reciprocal_rank_fusion(
        rankings=[
            ["a", "b", "c"],
            ["d", "e", "f"],
        ],
        top_k=3,
    )

    assert len(fused) == 3


def test_rrf_zero_top_k_returns_empty_list() -> None:
    assert reciprocal_rank_fusion([["a"]], top_k=0) == []
