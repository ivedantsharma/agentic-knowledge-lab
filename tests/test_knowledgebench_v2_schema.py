import pytest
from pydantic import ValidationError

from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
    KnowledgeChallenge,
)


def test_answerable_multihop_task_requires_chain() -> None:
    task = KnowledgeBenchV2Task(
        task_id="kbv2-001",
        question="What is the production backup cadence?",
        challenge_types={
            KnowledgeChallenge.MULTI_HOP,
            KnowledgeChallenge.DISTRACTOR,
        },
        should_answer=True,
        expected_answer="every six hours",
        supporting_document_ids={"org", "manual"},
        evidence_chain=["org", "manual"],
        distractor_document_ids={"legacy"},
    )

    assert task.should_answer is True
    assert task.evidence_chain == ["org", "manual"]


def test_unanswerable_task_has_no_supporting_documents() -> None:
    task = KnowledgeBenchV2Task(
        task_id="kbv2-002",
        question="Who owns the cafeteria menu service?",
        challenge_types={
            KnowledgeChallenge.UNANSWERABLE,
        },
        should_answer=False,
    )

    assert task.expected_answer is None
    assert not task.supporting_document_ids


def test_unanswerable_task_rejects_expected_answer() -> None:
    with pytest.raises(ValidationError):
        KnowledgeBenchV2Task(
            task_id="kbv2-003",
            question="Unknown fact?",
            challenge_types={
                KnowledgeChallenge.UNANSWERABLE,
            },
            should_answer=False,
            expected_answer="invented",
        )


def test_document_roles_must_not_overlap() -> None:
    with pytest.raises(ValidationError):
        KnowledgeBenchV2Task(
            task_id="kbv2-004",
            question="What is the current value?",
            challenge_types={
                KnowledgeChallenge.STALE_KNOWLEDGE,
            },
            should_answer=True,
            expected_answer="new",
            supporting_document_ids={"doc-current"},
            stale_document_ids={"doc-current"},
        )
