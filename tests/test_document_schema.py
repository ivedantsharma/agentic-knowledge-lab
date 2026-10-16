import pytest
from pydantic import ValidationError

from knowledgebench.documents.schema import KnowledgeDocument


def test_valid_document() -> None:
    document = KnowledgeDocument(
        document_id="doc_python",
        text="Python virtual environments isolate dependencies.",
        metadata={"source": "synthetic"},
    )

    assert document.document_id == "doc_python"


def test_document_id_is_trimmed() -> None:
    document = KnowledgeDocument(
        document_id="  doc_python  ",
        text="Some text",
    )

    assert document.document_id == "doc_python"


def test_blank_document_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        KnowledgeDocument(document_id="   ", text="Some text")


def test_blank_document_text_is_rejected() -> None:
    with pytest.raises(ValidationError):
        KnowledgeDocument(document_id="doc_python", text="   ")
