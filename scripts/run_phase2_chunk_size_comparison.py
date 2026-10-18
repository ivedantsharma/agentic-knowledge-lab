import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.ingestion.chunker import chunk_by_words
from knowledge_engine.ingestion.loader import load_source_documents_jsonl
from knowledgebench.evaluation.benchmark_evaluator import evaluate_retrieval_run
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.evidence_labeler import derive_chunk_task
from knowledgebench.tasks.evidence_schema import EvidenceTask
from scripts.cosine_similarity_exercise import cosine_similarity


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SOURCE_PATH = Path("data/processed/phase2_source_documents_v0.jsonl")
TASK_PATH = Path("data/processed/phase2_evidence_tasks_v0.json")


def load_evidence_tasks() -> list[EvidenceTask]:
    payload = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    return [EvidenceTask.model_validate(item) for item in payload]


def rank(query, chunk_ids, embeddings, model, top_k):
    query_embedding = model.encode(query).tolist()

    scored = [
        (
            chunk_id,
            cosine_similarity(query_embedding, embedding.tolist()),
        )
        for chunk_id, embedding in zip(chunk_ids, embeddings)
    ]

    scored.sort(key=lambda item: item[1], reverse=True)
    return [chunk_id for chunk_id, _ in scored[:top_k]]


def evaluate_configuration(
    documents,
    evidence_tasks,
    model,
    chunk_size_words: int,
    overlap_words: int,
) -> None:
    chunks = []

    for document in documents:
        chunks.extend(
            chunk_by_words(
                document,
                chunk_size_words=chunk_size_words,
                overlap_words=overlap_words,
            )
        )

    tasks = [
        derive_chunk_task(task, chunks)
        for task in evidence_tasks
    ]

    fragmented = [
        task.task_id
        for task in tasks
        if not task.relevant_document_ids
    ]

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
            metadata={
                "chunk_size_words": chunk_size_words,
                "overlap_words": overlap_words,
            },
        )
        for task in tasks
    ]

    answerable_tasks = [
        task
        for task in tasks
        if task.relevant_document_ids
    ]
    answerable_ids = {task.task_id for task in answerable_tasks}
    answerable_results = [
        result
        for result in results
        if result.task_id in answerable_ids
    ]

    at_1 = evaluate_retrieval_run(answerable_tasks, answerable_results, k=1)
    at_3 = evaluate_retrieval_run(answerable_tasks, answerable_results, k=3)

    print(
        f"chunk_size={chunk_size_words}, "
        f"overlap={overlap_words}"
    )
    print(f"chunks={len(chunks)}")
    print(f"fragmented_tasks={fragmented}")
    print(f"Recall@1={at_1.mean_recall_at_k:.4f}")
    print(f"Recall@3={at_3.mean_recall_at_k:.4f}")
    print(f"MRR={at_3.mean_reciprocal_rank:.4f}")

    for task, result in zip(tasks, results):
        print(f"  {task.task_id}")
        print(f"    relevant={sorted(task.relevant_document_ids)}")
        print(f"    retrieved={result.retrieved_document_ids}")

    print()


def main() -> None:
    documents = load_source_documents_jsonl(SOURCE_PATH)
    evidence_tasks = load_evidence_tasks()
    model = SentenceTransformer(MODEL_NAME)

    configurations = [
        (12, 0),
        (18, 0),
        (18, 6),
        (30, 0),
    ]

    for chunk_size_words, overlap_words in configurations:
        evaluate_configuration(
            documents,
            evidence_tasks,
            model,
            chunk_size_words,
            overlap_words,
        )


if __name__ == "__main__":
    main()
