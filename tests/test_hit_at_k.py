from knowledgebench.metrics.retrieval import hit_at_k


def test_hit_at_k_returns_one_when_any_relevant_item_is_found() -> None:
    assert hit_at_k(
        ["a", "x", "y"],
        {"a", "b"},
        k=1,
    ) == 1.0


def test_hit_at_k_returns_zero_when_no_relevant_item_is_found() -> None:
    assert hit_at_k(
        ["x", "y"],
        {"a", "b"},
        k=2,
    ) == 0.0


def test_hit_at_k_with_zero_k_returns_zero() -> None:
    assert hit_at_k(["a"], {"a"}, k=0) == 0.0
