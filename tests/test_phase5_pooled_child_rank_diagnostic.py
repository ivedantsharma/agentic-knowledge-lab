from scripts.run_phase5_pooled_child_rank_diagnostic import (
    reciprocal_rank,
)


def test_reciprocal_rank_for_child_rank() -> None:
    assert reciprocal_rank(1) == 1.0
    assert reciprocal_rank(2) == 0.5
    assert reciprocal_rank(None) == 0.0
