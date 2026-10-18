import pytest

from knowledgebench.evaluation.category_evaluator import evaluate_retrieval_by_category
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.schema import KnowledgeTask


def test_evaluate_retrieval_by_category() -> None:
    tasks = [
        KnowledgeTask(
            task_id="q1",
            question="Lexical one",
            relevant_document_ids={"a"},
            category="lexical",
        ),
        KnowledgeTask(
            task_id="q2",
            question="Semantic one",
            relevant_document_ids={"b"},
            category="semantic",
        ),
        KnowledgeTask(
            task_id="q3",
            question="Semantic two",
            relevant_document_ids={"c"},
            category="semantic",
        ),
    ]

    results = [
        RunResult(task_id="q1", retrieved_document_ids=["a", "x"]),
        RunResult(task_id="q2", retrieved_document_ids=["x", "b"]),
        RunResult(task_id="q3", retrieved_document_ids=["c", "x"]),
    ]

    report = evaluate_retrieval_by_category(tasks, results, k=1)

    assert report["lexical"]["recall@1"] == pytest.approx(1.0)
    assert report["lexical"]["mrr"] == pytest.approx(1.0)

    assert report["semantic"]["recall@1"] == pytest.approx(0.5)
    assert report["semantic"]["mrr"] == pytest.approx(0.75)
