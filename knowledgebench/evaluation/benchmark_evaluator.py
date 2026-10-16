from pydantic import BaseModel

from knowledgebench.evaluation.retrieval_evaluator import (
    mean_precision_at_k,
    mean_recall_at_k,
    mean_reciprocal_rank,
)
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.schema import KnowledgeTask


class BenchmarkRetrievalReport(BaseModel):
    """Aggregate retrieval metrics for one benchmark run."""

    mean_recall_at_k: float
    mean_precision_at_k: float
    mean_reciprocal_rank: float
    evaluated_tasks: int
    answerable_tasks: int
    unanswerable_tasks: int
    missing_results: int
    unanswerable_retrieval_rate: float


def evaluate_retrieval_run(
    tasks: list[KnowledgeTask],
    results: list[RunResult],
    k: int,
) -> BenchmarkRetrievalReport:
    """Evaluate retrieval outputs against KnowledgeBench task ground truth."""
    results_by_task_id = {
        result.task_id: result
        for result in results
    }

    answerable_tasks = [
        task
        for task in tasks
        if task.relevant_document_ids
    ]

    unanswerable_tasks = [
        task
        for task in tasks
        if not task.relevant_document_ids
    ]

    relevant_by_query = {
        task.task_id: task.relevant_document_ids
        for task in answerable_tasks
    }

    retrieved_by_query = {
        task.task_id: results_by_task_id.get(
            task.task_id,
            RunResult(task_id=task.task_id),
        ).retrieved_document_ids
        for task in answerable_tasks
    }

    task_ids = {task.task_id for task in tasks}
    result_ids = {result.task_id for result in results}

    unanswerable_with_retrieval = sum(
        1
        for task in unanswerable_tasks
        if results_by_task_id.get(
            task.task_id,
            RunResult(task_id=task.task_id),
        ).retrieved_document_ids
    )

    unanswerable_retrieval_rate = (
        unanswerable_with_retrieval / len(unanswerable_tasks)
        if unanswerable_tasks
        else 0.0
    )

    return BenchmarkRetrievalReport(
        mean_recall_at_k=mean_recall_at_k(
            retrieved_by_query,
            relevant_by_query,
            k,
        ),
        mean_precision_at_k=mean_precision_at_k(
            retrieved_by_query,
            relevant_by_query,
            k,
        ),
        mean_reciprocal_rank=mean_reciprocal_rank(
            retrieved_by_query,
            relevant_by_query,
        ),
        evaluated_tasks=len(tasks),
        answerable_tasks=len(answerable_tasks),
        unanswerable_tasks=len(unanswerable_tasks),
        missing_results=len(task_ids - result_ids),
        unanswerable_retrieval_rate=unanswerable_retrieval_rate,
    )
