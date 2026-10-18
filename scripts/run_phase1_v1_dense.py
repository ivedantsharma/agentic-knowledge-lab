from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.evaluation.benchmark_evaluator import evaluate_retrieval_run
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.loader import load_tasks_jsonl
from scripts.cosine_similarity_exercise import cosine_similarity


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TASKS_PATH = Path("data/processed/knowledgebench_phase1_v1_tasks.jsonl")
DOCUMENTS_PATH = Path("data/processed/knowledgebench_phase1_v1_documents.jsonl")


def rank_documents(
    query: str,
    document_ids: list[str],
    document_embeddings,
    model: SentenceTransformer,
    top_k: int,
) -> list[str]:
    query_embedding = model.encode(query).tolist()

    scored = [
        (
            document_id,
            cosine_similarity(query_embedding, embedding.tolist()),
        )
        for document_id, embedding in zip(document_ids, document_embeddings)
    ]

    scored.sort(key=lambda item: item[1], reverse=True)
    return [document_id for document_id, _ in scored[:top_k]]


def main() -> None:
    tasks = load_tasks_jsonl(TASKS_PATH)
    documents = load_documents_jsonl(DOCUMENTS_PATH)

    model = SentenceTransformer(MODEL_NAME)

    document_ids = [document.document_id for document in documents]
    document_texts = [document.text for document in documents]
    document_embeddings = model.encode(document_texts)

    results: list[RunResult] = []

    for task in tasks:
        retrieved_ids = rank_documents(
            query=task.question,
            document_ids=document_ids,
            document_embeddings=document_embeddings,
            model=model,
            top_k=3,
        )

        results.append(
            RunResult(
                task_id=task.task_id,
                retrieved_document_ids=retrieved_ids,
                tool_calls=1,
                metadata={"retriever": "dense_minilm"},
            )
        )

    report = evaluate_retrieval_run(tasks, results, k=3)

    print("KnowledgeBench Phase 1 v1 Dense")
    print(f"Answerable Recall@3: {report.mean_recall_at_k:.4f}")
    print(f"Answerable Precision@3: {report.mean_precision_at_k:.4f}")
    print(f"MRR: {report.mean_reciprocal_rank:.4f}")
    print(f"Unanswerable retrieval rate: {report.unanswerable_retrieval_rate:.4f}")
    print()

    for task, result in zip(tasks, results):
        print(f"{task.task_id} [{task.category}]")
        print(f"  relevant:  {sorted(task.relevant_document_ids)}")
        print(f"  retrieved: {result.retrieved_document_ids}")
        print()


if __name__ == "__main__":
    main()
