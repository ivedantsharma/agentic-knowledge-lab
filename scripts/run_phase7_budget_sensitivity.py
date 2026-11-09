import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document
from knowledgebench.evaluation.v2_retrieval_evaluator import (
    evaluate_v2_by_challenge,
    evaluate_v2_retrieval,
)
from knowledgebench.tasks.v2_schema import KnowledgeBenchV2Task

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_VALUES = [1, 3, 5]

DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_documents_v0.json"
)
TASKS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_tasks_v0.json"
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


def full_bm25_rankings(
    documents: list[KnowledgeBenchV2Document],
    tasks: list[KnowledgeBenchV2Task],
) -> dict[str, list[str]]:
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

    return {
        task.task_id: [
            document_id
            for document_id, _score
            in retriever.rank(
                task.question,
                top_k=len(documents),
            )
        ]
        for task in tasks
    }


def full_dense_rankings(
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


def print_budget_report(
    retriever_name: str,
    tasks: list[KnowledgeBenchV2Task],
    full_rankings: dict[str, list[str]],
) -> None:
    print(retriever_name)

    for k in TOP_K_VALUES:
        report = evaluate_v2_retrieval(
            tasks=tasks,
            retrieved_by_task=full_rankings,
            k=k,
        )

        print(f"k={k}")
        print(
            "  supporting_recall="
            f"{report.mean_supporting_recall_at_k:.4f}"
        )
        print(
            "  mrr="
            f"{report.mean_reciprocal_rank:.4f}"
        )
        print(
            "  chain_coverage="
            f"{report.mean_evidence_chain_coverage:.4f}"
        )
        print(
            "  distractor_hit_rate="
            f"{report.distractor_hit_rate:.4f}"
        )
        print(
            "  contradiction_hit_rate="
            f"{report.contradiction_hit_rate:.4f}"
        )
        print(
            "  stale_hit_rate="
            f"{report.stale_hit_rate:.4f}"
        )
        print(
            "  ambiguity_coverage="
            f"{report.mean_ambiguity_candidate_coverage:.4f}"
        )
        print(
            "  unanswerable_retrieval_rate="
            f"{report.unanswerable_retrieval_rate:.4f}"
        )

    print()


def print_challenge_budget_report(
    retriever_name: str,
    tasks: list[KnowledgeBenchV2Task],
    full_rankings: dict[str, list[str]],
) -> None:
    print(f"{retriever_name} challenge slices")

    for k in TOP_K_VALUES:
        reports = evaluate_v2_by_challenge(
            tasks=tasks,
            retrieved_by_task=full_rankings,
            k=k,
        )

        print(f"k={k}")

        for challenge in [
            "multi_hop",
            "stale_knowledge",
            "contradiction",
            "distractor",
            "ambiguity",
            "unanswerable",
        ]:
            report = reports[challenge]
            print(
                f"  {challenge}: "
                f"support={report.mean_supporting_recall_at_k:.4f}, "
                f"chain={report.mean_evidence_chain_coverage:.4f}, "
                f"distractor={report.distractor_hit_rate:.4f}, "
                f"contradiction={report.contradiction_hit_rate:.4f}, "
                f"stale={report.stale_hit_rate:.4f}, "
                f"ambiguity={report.mean_ambiguity_candidate_coverage:.4f}, "
                f"unanswerable={report.unanswerable_retrieval_rate:.4f}"
            )

    print()


def main() -> None:
    documents = load_documents()
    tasks = load_tasks()

    bm25_rankings = full_bm25_rankings(
        documents,
        tasks,
    )
    dense_rankings = full_dense_rankings(
        documents,
        tasks,
    )

    print_budget_report(
        "KnowledgeBench v2 Hard v0 — BM25 budget sensitivity",
        tasks,
        bm25_rankings,
    )
    print_budget_report(
        "KnowledgeBench v2 Hard v0 — Dense budget sensitivity",
        tasks,
        dense_rankings,
    )

    print_challenge_budget_report(
        "BM25",
        tasks,
        bm25_rankings,
    )
    print_challenge_budget_report(
        "Dense MiniLM",
        tasks,
        dense_rankings,
    )


if __name__ == "__main__":
    main()
