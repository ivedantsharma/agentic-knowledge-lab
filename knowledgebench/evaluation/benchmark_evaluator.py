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
    missing_results: int


def evaluate_retrieval_run(
    tasks: list[KnowledgeTask],
    results: list[RunResult],
    k: int,
) -> BenchmarkRetrievalReport:
    """Evaluate retrieval outputs against KnowledgeBench task ground truth."""
    relevant_by_query = {
        task.task_id: task.relevant_document_ids
        for task in tasks
    }

    retrieved_by_query = {
        result.task_id: result.retrieved_document_ids
        for result in results
    }

    task_ids = {task.task_id for task in tasks}
    result_ids = {result.task_id for result in results}

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
        missing_results=len(task_ids - result_ids),
    )
