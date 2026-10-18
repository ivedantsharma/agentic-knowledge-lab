import json
import sys
from pathlib import Path

from sentence_transformers import CrossEncoder, SentenceTransformer

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.rich_context_chunker import (
    chunk_by_rich_context,
)
from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)
from knowledge_engine.retrieval.reranker import (
    sort_by_reranker_scores,
)
from knowledgebench.evaluation.benchmark_evaluator import (
    evaluate_retrieval_run,
)
from knowledgebench.metrics.retrieval import hit_at_k
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.evidence_labeler import (
    derive_chunk_task,
)
from knowledgebench.tasks.evidence_schema import EvidenceTask
from scripts.cosine_similarity_exercise import (
    cosine_similarity,
)

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)
RERANKER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)

STRUCTURED_PATH = Path(
    "data/processed/"
    "phase2_structured_documents_context_v1.json"
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


def dense_rank(
    query: str,
    chunk_ids: list[str],
    chunk_embeddings,
    model: SentenceTransformer,
    top_k: int,
) -> list[str]:
    query_embedding = model.encode(query).tolist()

    scored = [
        (
            chunk_id,
            cosine_similarity(
                query_embedding,
                embedding.tolist(),
            ),
        )
        for chunk_id, embedding in zip(
            chunk_ids,
            chunk_embeddings,
        )
    ]

    scored.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        chunk_id
        for chunk_id, _ in scored[:top_k]
    ]


def main() -> None:
    documents = load_structured_documents_json(
        STRUCTURED_PATH
    )

    chunks = [
        chunk
        for document in documents
        for chunk in chunk_by_rich_context(document)
    ]

    tasks = [
        derive_chunk_task(task, chunks)
        for task in load_evidence_tasks()
    ]

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    reranker = CrossEncoder(
        RERANKER_MODEL
    )

    chunk_by_id = {
        chunk.chunk_id: chunk
        for chunk in chunks
    }

    chunk_ids = list(chunk_by_id)

    chunk_embeddings = embedding_model.encode(
        [
            chunk_by_id[chunk_id].text
            for chunk_id in chunk_ids
        ]
    )

    dense_results: list[RunResult] = []
    reranked_results: list[RunResult] = []

    for task in tasks:
        dense_candidates = dense_rank(
            task.question,
            chunk_ids,
            chunk_embeddings,
            embedding_model,
            top_k=3,
        )

        pairs = [
            (
                task.question,
                chunk_by_id[candidate_id].text,
            )
            for candidate_id in dense_candidates
        ]

        reranker_scores = reranker.predict(
            pairs
        ).tolist()

        reranked_ids = sort_by_reranker_scores(
            dense_candidates,
            reranker_scores,
        )

        dense_results.append(
            RunResult(
                task_id=task.task_id,
                retrieved_document_ids=dense_candidates,
                tool_calls=1,
                metadata={
                    "retriever": "dense_minilm",
                },
            )
        )

        reranked_results.append(
            RunResult(
                task_id=task.task_id,
                retrieved_document_ids=reranked_ids,
                tool_calls=2,
                metadata={
                    "retriever": "dense_plus_cross_encoder",
                    "reranker": RERANKER_MODEL,
                },
            )
        )

        print(task.task_id)
        print(f"  dense={dense_candidates}")
        print(
            "  reranker_scores="
            f"{[round(score, 6) for score in reranker_scores]}"
        )
        print(f"  reranked={reranked_ids}")
        print()

    for title, results in [
        ("Dense baseline", dense_results),
        ("Dense + cross-encoder reranker", reranked_results),
    ]:
        at_1 = evaluate_retrieval_run(
            tasks,
            results,
            k=1,
        )

        at_3 = evaluate_retrieval_run(
            tasks,
            results,
            k=3,
        )

        hit_1 = sum(
            hit_at_k(
                result.retrieved_document_ids,
                task.relevant_document_ids,
                1,
            )
            for task, result in zip(tasks, results)
        ) / len(tasks)

        print(title)
        print(
            f"Hit@1={hit_1:.4f}"
        )
        print(
            "Recall@1="
            f"{at_1.mean_recall_at_k:.4f}"
        )
        print(
            "Recall@3="
            f"{at_3.mean_recall_at_k:.4f}"
        )
        print(
            "MRR="
            f"{at_3.mean_reciprocal_rank:.4f}"
        )
        print()


if __name__ == "__main__":
    main()
