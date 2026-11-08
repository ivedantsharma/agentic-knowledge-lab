from scripts.run_phase5_deduplicated_neighbor_windows import (
    merge_chunk_window,
)


def test_merge_chunk_window_removes_overlap_duplication() -> None:
    section_text = "A B C D E F G H I J K L M N"

    chunks = [
        (0, 0, 10, "A B C D E F G H I J", 1.0),
        (1, 7, 14, "H I J K L M N", 0.9),
    ]

    merged = merge_chunk_window(
        section_text,
        chunks,
    )

    assert merged == "A B C D E F G H I J K L M N"
