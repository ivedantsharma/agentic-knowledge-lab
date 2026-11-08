from knowledge_engine.ingestion.hierarchical_chunker import (
    chunk_section,
)
from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)


def test_chunk_section_preserves_parent_context_in_text() -> None:
    document = StructuredDocument(
        document_id="manual_gamma",
        metadata={"title": "Cirrus Worker Manual"},
        sections=[
            DocumentSection(
                title="Dead Letter Handling",
                text=(
                    "A failed job is moved to CIRRUS-DLQ "
                    "after retry exhaustion."
                ),
            )
        ],
    )

    chunks = chunk_section(
        document,
        section_index=0,
        chunk_size_words=10,
    )

    assert chunks
    assert "Cirrus Worker Manual" in chunks[0].text
    assert "Dead Letter Handling" in chunks[0].text
    assert chunks[0].metadata["parent_document_id"] == "manual_gamma"
