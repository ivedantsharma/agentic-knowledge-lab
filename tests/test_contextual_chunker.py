from knowledge_engine.ingestion.contextual_chunker import (
    chunk_by_contextualized_section,
)
from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)


def test_contextualized_section_includes_document_and_section_context() -> None:
    document = StructuredDocument(
        document_id="manual_gamma",
        metadata={"title": "Cirrus Worker Manual"},
        sections=[
            DocumentSection(
                title="Dead Letter Handling",
                text=(
                    "A failed job is moved to CIRRUS-DLQ "
                    "after exhausting all retries."
                ),
            )
        ],
    )

    chunks = chunk_by_contextualized_section(document)

    assert len(chunks) == 1
    assert "Document: Cirrus Worker Manual." in chunks[0].text
    assert "Section: Dead Letter Handling." in chunks[0].text
    assert "CIRRUS-DLQ" in chunks[0].text
