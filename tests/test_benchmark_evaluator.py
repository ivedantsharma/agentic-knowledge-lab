import pytest

from knowledgebench.evaluation.benchmark_evaluator import evaluate_retrieval_run
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.schema import KnowledgeTask


def test_evaluate_retrieval_run() -> None:
    tasks = [
        KnowledgeTask(
            task_id="q1",
            question="Question one",
            relevant_document_ids={"a", "b"},
            category="direct",
        ),
        KnowledgeTask(
            task_id="q2",
            question="Question two",
            relevant_document_ids={"c"},
            category="direct",
        ),
    ]

    results = [
        RunResult(
            task_id="q1",
            retrieved_document_ids=["a", "x", "b"],
        ),
        RunResult(
            task_id="q2",
            retrieved_document_ids=["z", "c"],
        ),
    ]

    report = evaluate_retrieval_run(tasks, results, k=3)

    assert report.mean_recall_at_k == pytest.approx(1.0)
    assert report.mean_precision_at_k == pytest.approx(((2 / 3) + (1 / 2)) / 2)
    assert report.mean_reciprocal_rank == pytest.approx(0.75)
    assert report.evaluated_tasks == 2
    assert report.answerable_tasks == 2
    assert report.unanswerable_tasks == 0
    assert report.missing_results == 0
    assert report.unanswerable_retrieval_rate == pytest.approx(0.0)


def test_missing_run_result_counts_as_failure() -> None:
    tasks = [
        KnowledgeTask(
            task_id="q1",
            question="Question one",
            relevant_document_ids={"a"},
            category="direct",
        ),
        KnowledgeTask(
            task_id="q2",
            question="Question two",
            relevant_document_ids={"b"},
            category="direct",
        ),
    ]

    results = [
        RunResult(
            task_id="q1",
            retrieved_document_ids=["a"],
        ),
    ]

    report = evaluate_retrieval_run(tasks, results, k=1)

    assert report.mean_recall_at_k == pytest.approx(0.5)
    assert report.mean_reciprocal_rank == pytest.approx(0.5)
    assert report.evaluated_tasks == 2
    assert report.missing_results == 1


def test_unanswerable_tasks_are_scored_separately() -> None:
    tasks = [
        KnowledgeTask(
            task_id="q1",
            question="Answerable",
            relevant_document_ids={"a"},
            category="direct",
        ),
        KnowledgeTask(
            task_id="q2",
            question="Unanswerable",
            relevant_document_ids=set(),
            category="unanswerable",
        ),
    ]

    results = [
        RunResult(
            task_id="q1",
            retrieved_document_ids=["a"],
        ),
        RunResult(
            task_id="q2",
            retrieved_document_ids=["x", "y"],
        ),
    ]

    report = evaluate_retrieval_run(tasks, results, k=2)

    assert report.mean_recall_at_k == pytest.approx(1.0)
    assert report.mean_reciprocal_rank == pytest.approx(1.0)
    assert report.answerable_tasks == 1
    assert report.unanswerable_tasks == 1
    assert report.unanswerable_retrieval_rate == pytest.approx(1.0)
