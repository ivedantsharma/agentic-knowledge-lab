from knowledgebench.documents.v2_schema import (
    KnowledgeBenchV2Document,
)
from knowledgebench.evaluation.v2_audit import (
    audit_knowledgebench_v2,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
    KnowledgeChallenge,
)


def test_v2_audit_passes_valid_small_benchmark() -> None:
    documents = [
        KnowledgeBenchV2Document(
            document_id="current",
            title="Current",
            text="Current value.",
            source_type="manual",
            effective_at="2026-01-01",
        ),
        KnowledgeBenchV2Document(
            document_id="stale",
            title="Stale",
            text="Old value.",
            source_type="manual",
            effective_at="2025-01-01",
        ),
    ]
    tasks = [
        KnowledgeBenchV2Task(
            task_id="t1",
            question="What is current?",
            challenge_types={
                KnowledgeChallenge.STALE_KNOWLEDGE,
            },
            should_answer=True,
            expected_answer="Current value",
            supporting_document_ids={"current"},
            stale_document_ids={"stale"},
        )
    ]

    report = audit_knowledgebench_v2(
        documents,
        tasks,
    )

    assert report.passed is True
    assert report.missing_document_references == []


def test_v2_audit_detects_missing_document_reference() -> None:
    documents = [
        KnowledgeBenchV2Document(
            document_id="a",
            title="A",
            text="A.",
            source_type="manual",
        )
    ]
    tasks = [
        KnowledgeBenchV2Task(
            task_id="t2",
            question="What is A?",
            challenge_types={
                KnowledgeChallenge.DISTRACTOR,
            },
            should_answer=True,
            expected_answer="A",
            supporting_document_ids={"missing"},
            distractor_document_ids={"a"},
        )
    ]

    report = audit_knowledgebench_v2(
        documents,
        tasks,
    )

    assert report.passed is False
    assert report.missing_document_references == [
        "missing"
    ]
