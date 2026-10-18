import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.ingestion.contextual_chunker import (
    chunk_by_contextualized_section,
)
from knowledge_engine.ingestion.structure_chunker import chunk_by_section
from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)
from knowledgebench.evaluation.benchmark_evaluator import evaluate_retrieval_run
from knowledgebench.metrics.retrieval import hit_at_k
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.evidence_labeler import derive_chunk_task
from knowledgebench.tasks.evidence_schema import EvidenceTask
from scripts.cosine_similarity_exercise import cosine_similarity


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

STRUCTURED_PATH = Path(
    "data/processed/phase2_structured_documents_v0.json"
)
TASK_PATH = Path(
    "data/processed/phase2_evidence_tasks_v0.json"
)


def load_evidence_tasks() -> list[EvidenceTask]:
    payload = json.loads(
        TASK_PATH.read_text(encoding="utf-8")
    )

    return [
        EvidenceTask.model_validate(item)
        for item in payload
    ]


def rank(
    query: str,
    item_ids: list[str],
    embeddings,
    model: SentenceTransformer,
    top_k: int,
) -> list[str]:
    query_embedding = model.encode(query).tolist()

    scored = [
        (
            item_id,
            cosine_similarity(
                query_embedding,
                embedding.tolist(),
            ),
        )
        for item_id, embedding in zip(
            item_ids,
            embeddings,
        )
    ]

    scored.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        item_id
        for item_id, _ in scored[:top_k]
    ]


def evaluate_configuration(
    title: str,
    chunks,
    evidence_tasks,
    model: SentenceTransformer,
) -> None:
    tasks = [
        derive_chunk_task(task, chunks)
        for task in evidence_tasks
    ]

    chunk_ids = [
        chunk.chunk_id
        for chunk in chunks
    ]

    embeddings = model.encode(
        [chunk.text for chunk in chunks]
    )

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

    evaluable = [
        task
        for task in tasks
        if task.relevant_document_ids
    ]

    evaluable_ids = {
        task.task_id
        for task in evaluable
    }

    evaluable_results = [
        result
        for result in results
        if result.task_id in evaluable_ids
    ]

    at_1 = evaluate_retrieval_run(
        evaluable,
        evaluable_results,
        k=1,
    )

    at_3 = evaluate_retrieval_run(
        evaluable,
        evaluable_results,
        k=3,
    )

    hit_1 = sum(
        hit_at_k(
            result.retrieved_document_ids,
            task.relevant_document_ids,
            1,
        )
        for task, result in zip(tasks, results)
        if task.relevant_document_ids
    ) / len(evaluable)

    hit_3 = sum(
        hit_at_k(
            result.retrieved_document_ids,
            task.relevant_document_ids,
            3,
        )
        for task, result in zip(tasks, results)
        if task.relevant_document_ids
    ) / len(evaluable)

    print(title)
    print(f"chunks={len(chunks)}")
    print(f"Recall@1={at_1.mean_recall_at_k:.4f}")
    print(f"Recall@3={at_3.mean_recall_at_k:.4f}")
    print(f"Hit@1={hit_1:.4f}")
    print(f"Hit@3={hit_3:.4f}")
    print(f"MRR={at_3.mean_reciprocal_rank:.4f}")
    print()

    for task, result in zip(tasks, results):
        print(f"  {task.task_id}")
        print(
            f"    relevant="
            f"{sorted(task.relevant_document_ids)}"
        )
        print(
            f"    retrieved="
            f"{result.retrieved_document_ids}"
        )

    print()


def main() -> None:
    documents = load_structured_documents_json(
        STRUCTURED_PATH
    )
    evidence_tasks = load_evidence_tasks()

    model = SentenceTransformer(MODEL_NAME)

    plain_sections = [
        chunk
        for document in documents
        for chunk in chunk_by_section(document)
    ]

    contextualized_sections = [
        chunk
        for document in documents
        for chunk in chunk_by_contextualized_section(
            document
        )
    ]

    evaluate_configuration(
        "Plain section chunks",
        plain_sections,
        evidence_tasks,
        model,
    )

    evaluate_configuration(
        "Contextualized section chunks",
        contextualized_sections,
        evidence_tasks,
        model,
    )


if __name__ == "__main__":
    main()
