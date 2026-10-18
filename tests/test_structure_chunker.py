from knowledge_engine.ingestion.structure_chunker import chunk_by_section
from knowledge_engine.ingestion.structured_schema import DocumentSection, StructuredDocument


def test_chunk_by_section_preserves_section_context() -> None:
    document = StructuredDocument(
        document_id="manual",
        sections=[
            DocumentSection(
                title="Token Rotation",
                text="The current key identifier is KV-104.",
            ),
            DocumentSection(
                title="Cache Behavior",
                text="Metadata is cached for five minutes.",
            ),
        ],
    )

    chunks = chunk_by_section(document)

    assert len(chunks) == 2
    assert chunks[0].text == (
        "Token Rotation. The current key identifier is KV-104."
    )
    assert chunks[0].metadata["section_title"] == "Token Rotation"
    assert chunks[0].source_document_id == "manual"
