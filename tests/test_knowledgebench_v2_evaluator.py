from knowledgebench.evaluation.v2_retrieval_evaluator import (
    evaluate_v2_by_challenge,
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



def test_v2_evaluator_tracks_ambiguity_candidate_coverage() -> None:
    task = KnowledgeBenchV2Task(
        task_id="t3",
        question="What cache duration does Nimbus use?",
        challenge_types={
            KnowledgeChallenge.AMBIGUITY,
            KnowledgeChallenge.UNANSWERABLE,
        },
        should_answer=False,
        ambiguity_candidate_document_ids={"a", "b"},
    )

    report = evaluate_v2_retrieval(
        tasks=[task],
        retrieved_by_task={
            "t3": ["a", "other"],
        },
        k=2,
    )

    task_report = report.task_reports[0]

    assert (
        task_report.ambiguity_candidate_coverage
        == 0.5
    )
    assert (
        report.mean_ambiguity_candidate_coverage
        == 0.5
    )



def test_v2_evaluator_reports_per_challenge_slices() -> None:
    tasks = [
        KnowledgeBenchV2Task(
            task_id="m",
            question="Multi-hop?",
            challenge_types={
                KnowledgeChallenge.MULTI_HOP,
            },
            should_answer=True,
            expected_answer="x",
            supporting_document_ids={"a", "b"},
            evidence_chain=["a", "b"],
        ),
        KnowledgeBenchV2Task(
            task_id="u",
            question="Unknown?",
            challenge_types={
                KnowledgeChallenge.UNANSWERABLE,
            },
            should_answer=False,
        ),
    ]

    reports = evaluate_v2_by_challenge(
        tasks=tasks,
        retrieved_by_task={
            "m": ["a"],
            "u": ["other"],
        },
        k=1,
    )

    assert set(reports) == {
        "multi_hop",
        "unanswerable",
    }
    assert (
        reports["multi_hop"].mean_supporting_recall_at_k
        == 0.5
    )
    assert (
        reports["unanswerable"].unanswerable_retrieval_rate
        == 1.0
    )
