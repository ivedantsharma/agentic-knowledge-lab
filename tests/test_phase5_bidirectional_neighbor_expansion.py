from scripts.run_phase5_bidirectional_neighbor_expansion import (
    choose_radius_one,
)


def test_choose_radius_one_keeps_previous_top_and_next() -> None:
    scored_chunks = [
        (0, 0, 10, "zero", 0.2),
        (1, 7, 17, "one", 1.0),
        (2, 14, 24, "two", 0.1),
        (3, 21, 31, "three", 0.0),
    ]

    selected = choose_radius_one(
        top_chunk_index=1,
        scored_chunks=scored_chunks,
    )

    assert [item[0] for item in selected] == [0, 1, 2]


def test_choose_radius_one_handles_edge_chunk() -> None:
    scored_chunks = [
        (0, 0, 10, "zero", 1.0),
        (1, 7, 17, "one", 0.5),
    ]

    selected = choose_radius_one(
        top_chunk_index=0,
        scored_chunks=scored_chunks,
    )

    assert [item[0] for item in selected] == [0, 1]
