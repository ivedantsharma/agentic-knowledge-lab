from pathlib import Path


def test_phase5_two_level_beam_constants_are_small() -> None:
    script = Path(
        "scripts/run_phase5_parent2_child2_beam.py"
    ).read_text(encoding="utf-8")

    assert "PARENT_BEAM = 2" in script
    assert "CHILD_BEAM = 2" in script
