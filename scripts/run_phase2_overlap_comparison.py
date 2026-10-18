from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.ingestion.chunk_loader import load_chunks_jsonl
from knowledgebench.evaluation.benchmark_evaluator import evaluate_retrieval_run
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.loader import load_tasks_jsonl
from scripts.cosine_similarity_exercise import cosine_similarity


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

NO_OVERLAP_CHUNKS = Path("data/processed/phase2_chunks_v0.jsonl")
NO_OVERLAP_TASKS = Path("data/processed/phase2_chunk_tasks_v1.jsonl")

OVERLAP_CHUNKS = Path("data/processed/phase2_chunks_overlap6_v1.jsonl")
OVERLAP_TASKS = Path("data/processed/phase2_chunk_overlap6_tasks_v1.jsonl")


def rank(
    query: str,
    ids: list[str],
    embeddings,
    model: SentenceTransformer,
    top_k: int,
) -> list[str]:
    query_embedding = model.encode(query).tolist()

    scored = [
        (
            item_id,
            cosine_similarity(query_embedding, embedding.tolist()),
        )
        for item_id, embedding in zip(ids, embeddings)
    ]

    scored.sort(key=lambda item: item[1], reverse=True)
    return [item_id for item_id, _ in scored[:top_k]]


def evaluate_configuration(
    title: str,
    chunk_path: Path,
    task_path: Path,
    model: SentenceTransformer,
) -> None:
    chunks = load_chunks_jsonl(chunk_path)
    tasks = load_tasks_jsonl(task_path)

    chunk_ids = [chunk.chunk_id for chunk in chunks]
    embeddings = model.encode([chunk.text for chunk in chunks])

    results = [
        RunResult(
            task_id=task.task_id,
            retrieved_document_ids=rank(
                task.question,
                chunk_ids,
                embeddings,
                model,
                top_k=3,
            ),
            tool_calls=1,
            metadata={"retriever": "dense_minilm"},
        )
        for task in tasks
    ]

    at_1 = evaluate_retrieval_run(tasks, results, k=1)
    at_3 = evaluate_retrieval_run(tasks, results, k=3)

    print(title)
    print(f"Chunks indexed: {len(chunks)}")
    print(f"Recall@1: {at_1.mean_recall_at_k:.4f}")
    print(f"Recall@3: {at_3.mean_recall_at_k:.4f}")
    print(f"MRR: {at_3.mean_reciprocal_rank:.4f}")
    print()

    for task, result in zip(tasks, results):
        print(task.task_id)
        print(f"  relevant:  {sorted(task.relevant_document_ids)}")
        print(f"  retrieved: {result.retrieved_document_ids}")
        print()


def main() -> None:
    model = SentenceTransformer(MODEL_NAME)

    evaluate_configuration(
        "Phase 2 Fixed Chunks — 18 words, 0 overlap",
        NO_OVERLAP_CHUNKS,
        NO_OVERLAP_TASKS,
        model,
    )

    evaluate_configuration(
        "Phase 2 Fixed Chunks — 18 words, 6 overlap",
        OVERLAP_CHUNKS,
        OVERLAP_TASKS,
        model,
    )


if __name__ == "__main__":
    main()
