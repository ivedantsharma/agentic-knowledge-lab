import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.bm25 import (
    BM25Retriever,
)
from knowledge_engine.retrieval.vector_math import (
    cosine_similarity,
)
from knowledgebench.documents.v2_schema import (
    KnowledgeBenchV2Document,
)
from knowledgebench.evaluation.v2_retrieval_evaluator import (
    KnowledgeBenchV2RetrievalReport,
    evaluate_v2_retrieval,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3

DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_seed_documents_v0.json"
)
TASKS_PATH = Path(
    "data/processed/knowledgebench_v2_seed_tasks_v0.json"
)


def load_documents() -> list[KnowledgeBenchV2Document]:
    return [
        KnowledgeBenchV2Document.model_validate(
            item
        )
        for item in json.loads(
            DOCUMENTS_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def load_tasks() -> list[KnowledgeBenchV2Task]:
    return [
        KnowledgeBenchV2Task.model_validate(
            item
        )
        for item in json.loads(
            TASKS_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def run_bm25(
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
                top_k=TOP_K,
            )
        ]
        for task in tasks
    }


def run_dense(
    documents: list[KnowledgeBenchV2Document],
    tasks: list[KnowledgeBenchV2Task],
) -> dict[str, list[str]]:
    model = SentenceTransformer(
        MODEL_NAME
    )
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

    results: dict[str, list[str]] = {}

    for task in tasks:
        query_embedding = model.encode(
            task.question
        )

        scored = [
            (
                document_id,
                cosine_similarity(
                    query_embedding.tolist(),
                    embedding.tolist(),
                ),
            )
            for document_id, embedding
            in zip(
                document_ids,
                document_embeddings,
            )
        ]
        scored.sort(
            key=lambda item: item[1],
            reverse=True,
        )
        results[task.task_id] = [
            document_id
            for document_id, _score
            in scored[:TOP_K]
        ]

    return results


def print_report(
    name: str,
    report: KnowledgeBenchV2RetrievalReport,
    retrieved_by_task: dict[str, list[str]],
) -> None:
    print(name)

    for task_report in report.task_reports:
        print(task_report.task_id)
        print(
            "  retrieved="
            f"{retrieved_by_task[task_report.task_id]}"
        )
        print(
            "  supporting_recall@3="
            f"{task_report.supporting_recall_at_k:.4f}"
        )
        print(
            "  reciprocal_rank="
            f"{task_report.reciprocal_rank:.4f}"
        )
        print(
            "  evidence_chain_coverage="
            f"{task_report.evidence_chain_coverage:.4f}"
        )
        print(
            f"  distractor_hit={task_report.distractor_hit}"
        )
        print(
            "  contradiction_hit="
            f"{task_report.contradiction_hit}"
        )
        print(
            f"  stale_hit={task_report.stale_hit}"
        )
        print(
            f"  retrieved_any={task_report.retrieved_any}"
        )
        print()

    print("Aggregate")
    print(
        "MeanSupportingRecall@3="
        f"{report.mean_supporting_recall_at_k:.4f}"
    )
    print(
        "MRR="
        f"{report.mean_reciprocal_rank:.4f}"
    )
    print(
        "MeanEvidenceChainCoverage="
        f"{report.mean_evidence_chain_coverage:.4f}"
    )
    print(
        "DistractorHitRate="
        f"{report.distractor_hit_rate:.4f}"
    )
    print(
        "ContradictionHitRate="
        f"{report.contradiction_hit_rate:.4f}"
    )
    print(
        "StaleHitRate="
        f"{report.stale_hit_rate:.4f}"
    )
    print(
        "UnanswerableRetrievalRate="
        f"{report.unanswerable_retrieval_rate:.4f}"
    )
    print()


def main() -> None:
    documents = load_documents()
    tasks = load_tasks()

    bm25_results = run_bm25(
        documents,
        tasks,
    )
    dense_results = run_dense(
        documents,
        tasks,
    )

    bm25_report = evaluate_v2_retrieval(
        tasks,
        bm25_results,
        k=TOP_K,
    )
    dense_report = evaluate_v2_retrieval(
        tasks,
        dense_results,
        k=TOP_K,
    )

    print_report(
        "KnowledgeBench v2 Seed — BM25",
        bm25_report,
        bm25_results,
    )
    print_report(
        "KnowledgeBench v2 Seed — Dense MiniLM",
        dense_report,
        dense_results,
    )


if __name__ == "__main__":
    main()
