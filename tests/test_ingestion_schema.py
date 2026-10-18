import pytest
from pydantic import ValidationError

from knowledge_engine.ingestion.schema import DocumentChunk, SourceDocument


def test_valid_source_document() -> None:
    document = SourceDocument(
        document_id="doc-1",
        text="Some source text.",
    )

    assert document.document_id == "doc-1"


def test_blank_source_document_is_rejected() -> None:
    with pytest.raises(ValidationError):
        SourceDocument(document_id="doc-1", text="   ")


def test_valid_document_chunk() -> None:
    chunk = DocumentChunk(
        chunk_id="doc-1::chunk-0000",
        source_document_id="doc-1",
        chunk_index=0,
        text="Some chunk text.",
        start_word=0,
        end_word=3,
    )

    assert chunk.source_document_id == "doc-1"


def test_negative_chunk_position_is_rejected() -> None:
    with pytest.raises(ValidationError):
        DocumentChunk(
            chunk_id="doc-1::chunk-0000",
            source_document_id="doc-1",
            chunk_index=0,
            text="Some chunk text.",
            start_word=-1,
            end_word=3,
        )
