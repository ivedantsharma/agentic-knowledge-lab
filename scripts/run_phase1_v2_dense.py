from pathlib import Path

from sentence_transformers import SentenceTransformer

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

    model = SentenceTransformer(MODEL_NAME)

    document_ids = [document.document_id for document in documents]
    document_embeddings = model.encode([document.text for document in documents])

    results: list[RunResult] = []

    for task in tasks:
        query_embedding = model.encode(task.question).tolist()

        scored = [
            (
                document_id,
                cosine_similarity(query_embedding, embedding.tolist()),
            )
            for document_id, embedding in zip(document_ids, document_embeddings)
        ]

        scored.sort(key=lambda item: item[1], reverse=True)

        results.append(
            RunResult(
                task_id=task.task_id,
                retrieved_document_ids=[
                    document_id
                    for document_id, _ in scored[:3]
                ],
                tool_calls=1,
                metadata={"retriever": "dense_minilm"},
            )
        )

    print_reports(
        "KnowledgeBench Phase 1 v2 Dense",
        tasks,
        results,
    )


if __name__ == "__main__":
    main()
