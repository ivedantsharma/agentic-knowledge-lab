from knowledge_engine.ingestion.chunker import chunk_by_words
from knowledge_engine.ingestion.schema import (
    DocumentChunk,
    SourceDocument,
)
from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)


def chunk_section(
    document: StructuredDocument,
    section_index: int,
    chunk_size_words: int,
    overlap_words: int = 0,
) -> list[DocumentChunk]:
    """Chunk one structured section while preserving hierarchy metadata."""
    section: DocumentSection = document.sections[
        section_index
    ]

    section_source = SourceDocument(
        document_id=(
            f"{document.document_id}"
            f"::section-{section_index:04d}"
        ),
        text=section.text,
        metadata={
            **document.metadata,
            **section.metadata,
            "parent_document_id": document.document_id,
            "section_index": section_index,
            "section_title": section.title,
        },
    )

    chunks = chunk_by_words(
        section_source,
        chunk_size_words=chunk_size_words,
        overlap_words=overlap_words,
    )

    return [
        DocumentChunk(
            chunk_id=chunk.chunk_id,
            source_document_id=document.document_id,
            chunk_index=chunk.chunk_index,
            text=chunk.text,
            start_word=chunk.start_word,
            end_word=chunk.end_word,
            metadata={
                **chunk.metadata,
                "parent_document_id": document.document_id,
                "section_index": section_index,
                "section_title": section.title,
            },
        )
        for chunk in chunks
    ]
