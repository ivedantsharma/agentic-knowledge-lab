from collections import defaultdict

from knowledgebench.evaluation.retrieval_evaluator import (
    mean_precision_at_k,
    mean_recall_at_k,
    mean_reciprocal_rank,
)
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.schema import KnowledgeTask


def evaluate_retrieval_by_category(
    tasks: list[KnowledgeTask],
    results: list[RunResult],
    k: int,
) -> dict[str, dict[str, float]]:
    """Return retrieval metrics grouped by KnowledgeTask.category."""
    results_by_task_id = {
        result.task_id: result
        for result in results
    }

    tasks_by_category: dict[str, list[KnowledgeTask]] = defaultdict(list)

    for task in tasks:
        if task.relevant_document_ids:
            tasks_by_category[task.category].append(task)

    report: dict[str, dict[str, float]] = {}

    for category, category_tasks in tasks_by_category.items():
        relevant_by_query = {
            task.task_id: task.relevant_document_ids
            for task in category_tasks
        }

        retrieved_by_query = {
            task.task_id: results_by_task_id.get(
                task.task_id,
                RunResult(task_id=task.task_id),
            ).retrieved_document_ids
            for task in category_tasks
        }

        report[category] = {
            f"recall@{k}": mean_recall_at_k(
                retrieved_by_query,
                relevant_by_query,
                k,
            ),
            f"precision@{k}": mean_precision_at_k(
                retrieved_by_query,
                relevant_by_query,
                k,
            ),
            "mrr": mean_reciprocal_rank(
                retrieved_by_query,
                relevant_by_query,
            ),
            "task_count": float(len(category_tasks)),
        }

    return dict(report)
