from knowledge_engine.ingestion.rich_context_chunker import (
    chunk_by_rich_context,
)
from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)


def test_rich_context_chunk_uses_section_context() -> None:
    document = StructuredDocument(
        document_id="manual",
        metadata={"title": "Manual"},
        sections=[
            DocumentSection(
                title="Retries",
                context=(
                    "This section explains what happens "
                    "after retry attempts fail."
                ),
                text="The item is moved elsewhere.",
            )
        ],
    )

    chunks = chunk_by_rich_context(document)

    assert chunks[0].text.startswith(
        "This section explains what happens "
        "after retry attempts fail."
    )
    assert chunks[0].metadata["chunking_strategy"] == (
        "rich_context_section"
    )
