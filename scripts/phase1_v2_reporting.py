from knowledgebench.evaluation.benchmark_evaluator import evaluate_retrieval_run
from knowledgebench.evaluation.category_evaluator import evaluate_retrieval_by_category
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.schema import KnowledgeTask


def print_reports(
    title: str,
    tasks: list[KnowledgeTask],
    results: list[RunResult],
) -> None:
    print(title)

    overall_at_1 = evaluate_retrieval_run(tasks, results, k=1)
    overall_at_3 = evaluate_retrieval_run(tasks, results, k=3)
    by_category = evaluate_retrieval_by_category(tasks, results, k=1)

    print(f"Answerable Recall@1: {overall_at_1.mean_recall_at_k:.4f}")
    print(f"Answerable Recall@3: {overall_at_3.mean_recall_at_k:.4f}")
    print(f"MRR: {overall_at_3.mean_reciprocal_rank:.4f}")
    print(
        "Unanswerable retrieval rate: "
        f"{overall_at_3.unanswerable_retrieval_rate:.4f}"
    )
    print()

    print("Category-level Recall@1")
    for category, metrics in sorted(by_category.items()):
        print(
            f"{category}: "
            f"recall@1={metrics['recall@1']:.4f}, "
            f"mrr={metrics['mrr']:.4f}, "
            f"tasks={int(metrics['task_count'])}"
        )

    print()

    for task, result in zip(tasks, results):
        print(f"{task.task_id} [{task.category}]")
        print(f"  relevant:  {sorted(task.relevant_document_ids)}")
        print(f"  retrieved: {result.retrieved_document_ids}")
        print()
