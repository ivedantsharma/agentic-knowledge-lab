from knowledgebench.evaluation.v2_retrieval_evaluator import (
    evaluate_v2_retrieval,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
    KnowledgeChallenge,
)


def test_v2_evaluator_separates_support_and_adversarial_roles() -> None:
    task = KnowledgeBenchV2Task(
        task_id="t1",
        question="What is current?",
        challenge_types={
            KnowledgeChallenge.MULTI_HOP,
            KnowledgeChallenge.DISTRACTOR,
            KnowledgeChallenge.STALE_KNOWLEDGE,
        },
        should_answer=True,
        expected_answer="new",
        supporting_document_ids={"a", "b"},
        evidence_chain=["a", "b"],
        distractor_document_ids={"d"},
        stale_document_ids={"s"},
    )

    report = evaluate_v2_retrieval(
        tasks=[task],
        retrieved_by_task={
            "t1": ["a", "s", "d"],
        },
        k=3,
    )

    task_report = report.task_reports[0]

    assert task_report.supporting_recall_at_k == 0.5
    assert task_report.reciprocal_rank == 1.0
    assert task_report.evidence_chain_coverage == 0.5
    assert task_report.distractor_hit is True
    assert task_report.stale_hit is True
    assert report.stale_hit_rate == 1.0
    assert report.distractor_hit_rate == 1.0


def test_v2_evaluator_tracks_unanswerable_retrieval() -> None:
    task = KnowledgeBenchV2Task(
        task_id="t2",
        question="Unknown?",
        challenge_types={
            KnowledgeChallenge.UNANSWERABLE,
        },
        should_answer=False,
    )

    report = evaluate_v2_retrieval(
        tasks=[task],
        retrieved_by_task={
            "t2": ["anything"],
        },
        k=3,
    )

    assert (
        report.unanswerable_retrieval_rate
        == 1.0
    )
