from pathlib import Path

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.runs.schema import RunResult
from knowledgebench.tasks.loader import load_tasks_jsonl
from scripts.phase1_v2_reporting import print_reports


TASKS_PATH = Path("data/processed/knowledgebench_phase1_v2_tasks.jsonl")
DOCUMENTS_PATH = Path("data/processed/knowledgebench_phase1_v2_documents.jsonl")


def main() -> None:
    tasks = load_tasks_jsonl(TASKS_PATH)
    documents = load_documents_jsonl(DOCUMENTS_PATH)

    retriever = BM25Retriever(
        document_ids=[document.document_id for document in documents],
        document_texts=[document.text for document in documents],
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

    print_reports(
        "KnowledgeBench Phase 1 v2 BM25",
        tasks,
        results,
    )


if __name__ == "__main__":
    main()
