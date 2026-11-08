from scripts.run_phase5_neighbor_expansion import choose_neighbor


def test_choose_neighbor_prefers_best_adjacent_chunk() -> None:
    scored_chunks = [
        (0, "c0", "zero", 0.4),
        (1, "c1", "one", 1.0),
        (2, "c2", "two", 0.8),
    ]

    neighbor = choose_neighbor(
        top_chunk_index=1,
        scored_chunks=scored_chunks,
    )

    assert neighbor is not None
    assert neighbor[1] == "c2"


def test_choose_neighbor_returns_none_for_single_chunk() -> None:
    scored_chunks = [
        (0, "c0", "zero", 1.0),
    ]

    assert choose_neighbor(0, scored_chunks) is None
