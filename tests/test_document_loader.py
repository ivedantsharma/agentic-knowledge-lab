import json

import pytest

from knowledgebench.documents.loader import DocumentLoadError, load_documents_jsonl


def test_load_documents_jsonl(tmp_path) -> None:
    path = tmp_path / "documents.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "document_id": "doc_a",
                        "text": "Document A",
                    }
                ),
                json.dumps(
                    {
                        "document_id": "doc_b",
                        "text": "Document B",
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    documents = load_documents_jsonl(path)

    assert len(documents) == 2
    assert documents[0].document_id == "doc_a"


def test_duplicate_document_id_is_rejected(tmp_path) -> None:
    path = tmp_path / "documents.jsonl"
    path.write_text(
        "\n".join(
            [
                '{"document_id":"doc_a","text":"A"}',
                '{"document_id":"doc_a","text":"B"}',
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(DocumentLoadError, match="Duplicate document_id"):
        load_documents_jsonl(path)


def test_invalid_document_reports_line_number(tmp_path) -> None:
    path = tmp_path / "documents.jsonl"
    path.write_text(
        '{"document_id":"doc_a","text":"   "}\n',
        encoding="utf-8",
    )

    with pytest.raises(DocumentLoadError, match="line 1"):
        load_documents_jsonl(path)
