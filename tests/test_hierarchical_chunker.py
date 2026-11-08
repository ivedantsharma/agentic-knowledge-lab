from knowledge_engine.ingestion.hierarchical_chunker import (
    chunk_section,
)
from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)


def test_chunk_section_preserves_parent_and_section_metadata() -> None:
    document = StructuredDocument(
        document_id="manual",
        metadata={"title": "Manual"},
        sections=[
            DocumentSection(
                title="Policy",
                text=(
                    "one two three four five six "
                    "seven eight nine ten eleven twelve"
                ),
            )
        ],
    )

    chunks = chunk_section(
        document,
        section_index=0,
        chunk_size_words=6,
    )

    assert len(chunks) == 2
    assert all(
        chunk.source_document_id == "manual"
        for chunk in chunks
    )
    assert all(
        chunk.metadata["section_title"] == "Policy"
        for chunk in chunks
    )
    assert all(
        chunk.metadata["section_index"] == 0
        for chunk in chunks
    )
