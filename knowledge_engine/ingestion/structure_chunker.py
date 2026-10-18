from knowledge_engine.ingestion.schema import DocumentChunk
from knowledge_engine.ingestion.structured_schema import StructuredDocument


def chunk_by_section(document: StructuredDocument) -> list[DocumentChunk]:
    """Create one retrieval chunk per document section."""
    chunks: list[DocumentChunk] = []
    word_offset = 0

    for index, section in enumerate(document.sections):
        section_text = f"{section.title}. {section.text}".strip()
        word_count = len(section_text.split())

        chunks.append(
            DocumentChunk(
                chunk_id=f"{document.document_id}::section-{index:04d}",
                source_document_id=document.document_id,
                chunk_index=index,
                text=section_text,
                start_word=word_offset,
                end_word=word_offset + word_count,
                metadata={
                    **document.metadata,
                    **section.metadata,
                    "section_title": section.title,
                    "chunking_strategy": "section",
                },
            )
        )

        word_offset += word_count

    return chunks
