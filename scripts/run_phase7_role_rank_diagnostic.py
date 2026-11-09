import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document
from knowledgebench.tasks.v2_schema import KnowledgeBenchV2Task

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_seed_documents_v0.json"
)
TASKS_PATH = Path(
    "data/processed/knowledgebench_v2_seed_tasks_v0.json"
)


def load_documents() -> list[KnowledgeBenchV2Document]:
    return [
        KnowledgeBenchV2Document.model_validate(item)
        for item in json.loads(
            DOCUMENTS_PATH.read_text(encoding="utf-8")
        )
    ]


def load_tasks() -> list[KnowledgeBenchV2Task]:
    return [
        KnowledgeBenchV2Task.model_validate(item)
        for item in json.loads(
            TASKS_PATH.read_text(encoding="utf-8")
        )
    ]


def rank_bm25(
    documents: list[KnowledgeBenchV2Document],
    task: KnowledgeBenchV2Task,
) -> list[str]:
    retriever = BM25Retriever(
        document_ids=[
            document.document_id
            for document in documents
        ],
        document_texts=[
            document.text
            for document in documents
        ],
    )
    return [
        document_id
        for document_id, _score
        in retriever.rank(
            task.question,
            top_k=len(documents),
        )
    ]


def rank_dense(
    documents: list[KnowledgeBenchV2Document],
    tasks: list[KnowledgeBenchV2Task],
) -> dict[str, list[str]]:
    model = SentenceTransformer(MODEL_NAME)

    document_ids = [
        document.document_id
        for document in documents
    ]
    document_embeddings = model.encode(
        [
            document.text
            for document in documents
        ]
    )

    rankings: dict[str, list[str]] = {}

    for task in tasks:
        query_embedding = model.encode(
            task.question
        ).tolist()

        scored = [
            (
                document_id,
                cosine_similarity(
                    query_embedding,
                    embedding.tolist(),
                ),
            )
            for document_id, embedding in zip(
                document_ids,
                document_embeddings,
            )
        ]
        scored.sort(
            key=lambda item: item[1],
            reverse=True,
        )
        rankings[task.task_id] = [
            document_id
            for document_id, _score in scored
        ]

    return rankings


def rank_of(
    ranking: list[str],
    document_id: str,
) -> int:
    return ranking.index(document_id) + 1


def print_role_ranks(
    name: str,
    tasks: list[KnowledgeBenchV2Task],
    rankings: dict[str, list[str]],
) -> None:
    print(name)

    for task in tasks:
        ranking = rankings[task.task_id]

        print(task.task_id)
        print(f"  ranking={ranking}")

        for role_name, document_ids in [
            (
                "supporting",
                task.supporting_document_ids,
            ),
            (
                "distractor",
                task.distractor_document_ids,
            ),
            (
                "contradicting",
                task.contradicting_document_ids,
            ),
            (
                "stale",
                task.stale_document_ids,
            ),
        ]:
            if not document_ids:
                continue

            role_ranks = {
                document_id: rank_of(
                    ranking,
                    document_id,
                )
                for document_id in sorted(document_ids)
            }
            print(
                f"  {role_name}_ranks={role_ranks}"
            )

        print()


def main() -> None:
    documents = load_documents()
    tasks = load_tasks()

    bm25_rankings = {
        task.task_id: rank_bm25(
            documents,
            task,
        )
        for task in tasks
    }
    dense_rankings = rank_dense(
        documents,
        tasks,
    )

    print_role_ranks(
        "KnowledgeBench v2 Role-Rank Diagnostic — BM25",
        tasks,
        bm25_rankings,
    )
    print_role_ranks(
        "KnowledgeBench v2 Role-Rank Diagnostic — Dense MiniLM",
        tasks,
        dense_rankings,
    )


if __name__ == "__main__":
    main()
