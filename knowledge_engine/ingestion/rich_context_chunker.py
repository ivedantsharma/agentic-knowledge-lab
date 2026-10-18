from knowledge_engine.ingestion.schema import DocumentChunk
from knowledge_engine.ingestion.structured_schema import StructuredDocument


def chunk_by_rich_context(
    document: StructuredDocument,
) -> list[DocumentChunk]:
    """Create section chunks with pre-authored chunk-specific context."""
    chunks: list[DocumentChunk] = []
    word_offset = 0

    document_title = str(
        document.metadata.get("title", document.document_id)
    )

    for index, section in enumerate(document.sections):
        base_text = f"{section.title}. {section.text}".strip()
        word_count = len(base_text.split())

        context = section.context or (
            f"This section belongs to {document_title}."
        )

        retrieval_text = (
            f"{context} "
            f"{section.title}. "
            f"{section.text}"
        )

        chunks.append(
            DocumentChunk(
                chunk_id=(
                    f"{document.document_id}"
                    f"::rich-context-section-{index:04d}"
                ),
                source_document_id=document.document_id,
                chunk_index=index,
                text=retrieval_text,
                start_word=word_offset,
                end_word=word_offset + word_count,
                metadata={
                    **document.metadata,
                    **section.metadata,
                    "section_title": section.title,
                    "chunking_strategy": "rich_context_section",
                    "chunk_context": context,
                },
            )
        )

        word_offset += word_count

    return chunks
