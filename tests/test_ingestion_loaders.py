import json

import pytest

from knowledge_engine.ingestion.chunk_loader import ChunkLoadError, load_chunks_jsonl
from knowledge_engine.ingestion.loader import SourceDocumentLoadError, load_source_documents_jsonl


def test_load_source_documents_jsonl(tmp_path) -> None:
    path = tmp_path / "sources.jsonl"
    path.write_text(
        json.dumps({"document_id": "doc-1", "text": "hello world"}) + "\n",
        encoding="utf-8",
    )

    documents = load_source_documents_jsonl(path)

    assert len(documents) == 1
    assert documents[0].document_id == "doc-1"


def test_duplicate_source_document_id_is_rejected(tmp_path) -> None:
    path = tmp_path / "sources.jsonl"
    path.write_text(
        "\n".join(
            [
                '{"document_id":"doc-1","text":"A"}',
                '{"document_id":"doc-1","text":"B"}',
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(SourceDocumentLoadError, match="Duplicate document_id"):
        load_source_documents_jsonl(path)


def test_load_chunks_jsonl(tmp_path) -> None:
    path = tmp_path / "chunks.jsonl"
    path.write_text(
        json.dumps(
            {
                "chunk_id": "doc-1::chunk-0000",
                "source_document_id": "doc-1",
                "chunk_index": 0,
                "text": "hello world",
                "start_word": 0,
                "end_word": 2,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    chunks = load_chunks_jsonl(path)

    assert len(chunks) == 1
    assert chunks[0].chunk_id == "doc-1::chunk-0000"


def test_duplicate_chunk_id_is_rejected(tmp_path) -> None:
    path = tmp_path / "chunks.jsonl"
    line = json.dumps(
        {
            "chunk_id": "doc-1::chunk-0000",
            "source_document_id": "doc-1",
            "chunk_index": 0,
            "text": "hello",
            "start_word": 0,
            "end_word": 1,
        }
    )

    path.write_text(line + "\n" + line + "\n", encoding="utf-8")

    with pytest.raises(ChunkLoadError, match="Duplicate chunk_id"):
        load_chunks_jsonl(path)
