from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.hybrid import reciprocal_rank_fusion
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.loader import load_tasks_jsonl
from scripts.cosine_similarity_exercise import cosine_similarity
from scripts.phase1_v2_reporting import print_reports


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TASKS_PATH = Path("data/processed/knowledgebench_phase1_v2_tasks.jsonl")
DOCUMENTS_PATH = Path("data/processed/knowledgebench_phase1_v2_documents.jsonl")


def main() -> None:
    tasks = load_tasks_jsonl(TASKS_PATH)
    documents = load_documents_jsonl(DOCUMENTS_PATH)

    document_ids = [document.document_id for document in documents]
    document_texts = [document.text for document in documents]

    bm25 = BM25Retriever(
        document_ids=document_ids,
        document_texts=document_texts,
    )

    model = SentenceTransformer(MODEL_NAME)
    document_embeddings = model.encode(document_texts)

    results: list[RunResult] = []

    for task in tasks:
        bm25_ranking = [
            document_id
            for document_id, _ in bm25.rank(task.question, top_k=len(documents))
        ]

        query_embedding = model.encode(task.question).tolist()

        dense_scored = [
            (
                document_id,
                cosine_similarity(query_embedding, embedding.tolist()),
            )
            for document_id, embedding in zip(document_ids, document_embeddings)
        ]
        dense_scored.sort(key=lambda item: item[1], reverse=True)
        dense_ranking = [
            document_id
            for document_id, _ in dense_scored
        ]

        fused = reciprocal_rank_fusion(
            rankings=[bm25_ranking, dense_ranking],
            top_k=3,
        )

        results.append(
            RunResult(
                task_id=task.task_id,
                retrieved_document_ids=[
                    document_id
                    for document_id, _ in fused
                ],
                tool_calls=2,
                metadata={
                    "retriever": "hybrid_rrf",
                    "components": ["bm25", "dense_minilm"],
                    "rrf_k": 60,
                },
            )
        )

    print_reports(
        "KnowledgeBench Phase 1 v2 Hybrid RRF",
        tasks,
        results,
    )


if __name__ == "__main__":
    main()
