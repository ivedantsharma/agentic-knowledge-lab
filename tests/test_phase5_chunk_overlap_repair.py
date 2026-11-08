from knowledge_engine.ingestion.hierarchical_chunker import (
    chunk_section,
)
from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)


def test_overlap_can_preserve_boundary_spanning_phrase() -> None:
    document = StructuredDocument(
        document_id="manual_beta",
        metadata={"title": "Borealis Storage Manual"},
        sections=[
            DocumentSection(
                title="Backup Policy",
                text=(
                    "Full backups run every Sunday, while "
                    "incremental backups run every six hours."
                ),
            )
        ],
    )

    chunks = chunk_section(
        document,
        section_index=0,
        chunk_size_words=10,
        overlap_words=3,
    )

    raw_chunks = [
        str(chunk.metadata["raw_chunk_text"])
        for chunk in chunks
    ]

    assert any(
        "every six hours" in text
        for text in raw_chunks
    )
