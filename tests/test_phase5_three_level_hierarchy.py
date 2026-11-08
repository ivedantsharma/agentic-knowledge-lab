from pathlib import Path


def test_phase5_three_level_baseline_settings() -> None:
    script = Path(
        "scripts/run_phase5_three_level_hierarchy.py"
    ).read_text(encoding="utf-8")

    assert "PARENT_BEAM = 2" in script
    assert "SECTION_BEAM = 2" in script
    assert "CHUNK_SIZE_WORDS = 10" in script
    assert "CHUNK_BEAM = 2" in script
