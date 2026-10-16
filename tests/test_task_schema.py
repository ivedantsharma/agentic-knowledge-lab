import pytest
from pydantic import ValidationError

from knowledgebench.tasks.schema import KnowledgeTask


def test_valid_knowledge_task() -> None:
    task = KnowledgeTask(
        task_id="kb-001",
        question="How do Python virtual environments help?",
        relevant_document_ids={"doc_python"},
        category="semantic_paraphrase",
        expected_answer="They isolate project dependencies.",
        metadata={"difficulty": "easy"},
    )

    assert task.task_id == "kb-001"
    assert task.relevant_document_ids == {"doc_python"}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("task_id", "   "),
        ("question", ""),
        ("category", "  "),
    ],
)
def test_blank_required_text_fields_are_rejected(field: str, value: str) -> None:
    kwargs = {
        "task_id": "kb-001",
        "question": "A valid question",
        "category": "direct",
    }
    kwargs[field] = value

    with pytest.raises(ValidationError):
        KnowledgeTask(**kwargs)


def test_unanswerable_task_can_have_no_relevant_documents() -> None:
    task = KnowledgeTask(
        task_id="kb-002",
        question="What is the launch date of a product that does not exist?",
        relevant_document_ids=set(),
        category="unanswerable",
        expected_answer=None,
    )

    assert task.relevant_document_ids == set()


def test_metadata_defaults_to_empty_dict() -> None:
    task = KnowledgeTask(
        task_id="kb-003",
        question="What is BM25?",
        category="direct",
    )

    assert task.metadata == {}
