from pathlib import Path


def test_phase5_per_section_chunk_diagnostic_uses_overlap() -> None:
    script = Path(
        "scripts/run_phase5_per_section_chunk_diagnostic.py"
    ).read_text(encoding="utf-8")

    assert "CHUNK_OVERLAP_WORDS = 3" in script
    assert "SECTION_BEAM = 2" in script
