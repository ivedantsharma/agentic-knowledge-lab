from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)
from knowledge_engine.retrieval.hierarchical import render_section


def test_cross_encoder_candidate_rendering_keeps_parent_context() -> None:
    document = StructuredDocument(
        document_id="manual_gamma",
        metadata={"title": "Cirrus Worker Manual"},
        sections=[
            DocumentSection(
                title="Dead Letter Handling",
                text="Jobs are moved to CIRRUS-DLQ.",
            )
        ],
    )

    candidate = render_section(
        document,
        document.sections[0],
    )

    assert "Cirrus Worker Manual" in candidate
    assert "Dead Letter Handling" in candidate
    assert "CIRRUS-DLQ" in candidate