from pathlib import Path

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.evaluation.benchmark_evaluator import evaluate_retrieval_run
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.loader import load_tasks_jsonl


TASKS_PATH = Path("data/processed/knowledgebench_phase1_v0.jsonl")
DOCUMENTS_PATH = Path("data/processed/knowledgebench_phase1_documents_v0.jsonl")


def main() -> None:
    tasks = load_tasks_jsonl(TASKS_PATH)
    documents = load_documents_jsonl(DOCUMENTS_PATH)

    document_ids = [
        document.document_id
        for document in documents
    ]
    document_texts = [
        document.text
        for document in documents
    ]

    retriever = BM25Retriever(
        document_ids=document_ids,
        document_texts=document_texts,
    )

    results: list[RunResult] = []

    for task in tasks:
        ranked = retriever.rank(task.question, top_k=3)

        results.append(
            RunResult(
                task_id=task.task_id,
                retrieved_document_ids=[
                    document_id
                    for document_id, _ in ranked
                ],
                tool_calls=1,
                metadata={"retriever": "bm25"},
            )
        )

    report = evaluate_retrieval_run(tasks, results, k=3)

    print("KnowledgeBench Phase 1 BM25 Baseline")
    print(f"Tasks evaluated: {report.evaluated_tasks}")
    print(f"Answerable tasks: {report.answerable_tasks}")
    print(f"Unanswerable tasks: {report.unanswerable_tasks}")
    print(f"Missing results: {report.missing_results}")
    print()
    print("Answerable-task retrieval metrics")
    print(f"Mean Recall@3: {report.mean_recall_at_k:.4f}")
    print(f"Mean Precision@3: {report.mean_precision_at_k:.4f}")
    print(f"MRR: {report.mean_reciprocal_rank:.4f}")
    print()
    print("Unanswerable-task diagnostic")
    print(
        "Unanswerable retrieval rate: "
        f"{report.unanswerable_retrieval_rate:.4f}"
    )
    print()

    for task, result in zip(tasks, results):
        print(f"{task.task_id}: {task.question}")
        print(f"  relevant:  {sorted(task.relevant_document_ids)}")
        print(f"  retrieved: {result.retrieved_document_ids}")
        print()


if __name__ == "__main__":
    main()
