from knowledge_engine.ingestion.schema import DocumentChunk
from knowledge_engine.ingestion.structured_schema import StructuredDocument


def chunk_by_contextualized_section(
    document: StructuredDocument,
) -> list[DocumentChunk]:
    """Create one section chunk with deterministic parent context prepended."""
    chunks: list[DocumentChunk] = []
    word_offset = 0

    document_title = str(
        document.metadata.get("title", document.document_id)
    )

    for index, section in enumerate(document.sections):
        base_text = f"{section.title}. {section.text}".strip()

        contextualized_text = (
            f"Document: {document_title}. "
            f"Section: {section.title}. "
            f"{section.text}"
        )

        word_count = len(base_text.split())

        chunks.append(
            DocumentChunk(
                chunk_id=(
                    f"{document.document_id}"
                    f"::context-section-{index:04d}"
                ),
                source_document_id=document.document_id,
                chunk_index=index,
                text=contextualized_text,
                start_word=word_offset,
                end_word=word_offset + word_count,
                metadata={
                    **document.metadata,
                    **section.metadata,
                    "section_title": section.title,
                    "chunking_strategy": "contextualized_section",
                    "context_prefix": (
                        f"Document: {document_title}. "
                        f"Section: {section.title}."
                    ),
                },
            )
        )

        word_offset += word_count

    return chunks
