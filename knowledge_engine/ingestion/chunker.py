from knowledge_engine.ingestion.schema import DocumentChunk, SourceDocument


def chunk_by_words(
    document: SourceDocument,
    chunk_size_words: int,
    overlap_words: int = 0,
) -> list[DocumentChunk]:
    """Split a source document into deterministic word-based chunks."""
    if chunk_size_words <= 0:
        raise ValueError("chunk_size_words must be greater than zero")

    if overlap_words < 0:
        raise ValueError("overlap_words must be zero or greater")

    if overlap_words >= chunk_size_words:
        raise ValueError("overlap_words must be smaller than chunk_size_words")

    words = document.text.split()

    if not words:
        return []

    stride = chunk_size_words - overlap_words
    chunks: list[DocumentChunk] = []

    for chunk_index, start_word in enumerate(range(0, len(words), stride)):
        end_word = min(start_word + chunk_size_words, len(words))
        chunk_words = words[start_word:end_word]

        if not chunk_words:
            continue

        chunks.append(
            DocumentChunk(
                chunk_id=f"{document.document_id}::chunk-{chunk_index:04d}",
                source_document_id=document.document_id,
                chunk_index=chunk_index,
                text=" ".join(chunk_words),
                start_word=start_word,
                end_word=end_word,
                metadata={
                    **document.metadata,
                    "chunk_size_words": chunk_size_words,
                    "overlap_words": overlap_words,
                },
            )
        )

        if end_word == len(words):
            break

    return chunks
