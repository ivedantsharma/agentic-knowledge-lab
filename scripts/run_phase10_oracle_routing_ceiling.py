import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.hybrid import (
    reciprocal_rank_fusion,
)
from knowledge_engine.retrieval.vector_math import (
    cosine_similarity,
)
from knowledgebench.documents.v2_schema import (
    KnowledgeBenchV2Document,
)
from knowledgebench.evaluation.routing_evaluator import (
    RetrievalStrategyTaskScore,
    evaluate_routing_oracle,
)
from knowledgebench.evaluation.v2_retrieval_evaluator import (
    evaluate_v2_retrieval,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3

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
            DOCUMENTS_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def load_tasks() -> list[KnowledgeBenchV2Task]:
    return [
        KnowledgeBenchV2Task.model_validate(item)
        for item in json.loads(
            TASKS_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def build_rankings(
    documents: list[KnowledgeBenchV2Document],
    tasks: list[KnowledgeBenchV2Task],
) -> dict[str, dict[str, list[str]]]:
    document_ids = [
        document.document_id
        for document in documents
    ]
    document_texts = [
        document.text
        for document in documents
    ]

    bm25 = BM25Retriever(
        document_ids=document_ids,
        document_texts=document_texts,
    )

    model = SentenceTransformer(
        MODEL_NAME
    )
    document_embeddings = model.encode(
        document_texts
    )

    results = {
        "bm25": {},
        "dense": {},
        "hybrid_rrf": {},
    }

    for task in tasks:
        bm25_full = [
            document_id
            for document_id, _score
            in bm25.rank(
                task.question,
                top_k=len(documents),
            )
        ]

        query_embedding = model.encode(
            task.question
        ).tolist()

        dense_scored = [
            (
                document_id,
                cosine_similarity(
                    query_embedding,
                    embedding.tolist(),
                ),
            )
            for document_id, embedding
            in zip(
                document_ids,
                document_embeddings,
            )
        ]
        dense_scored.sort(
            key=lambda item: item[1],
            reverse=True,
        )
        dense_full = [
            document_id
            for document_id, _score
            in dense_scored
        ]

        hybrid = reciprocal_rank_fusion(
            rankings=[
                bm25_full,
                dense_full,
            ],
            top_k=TOP_K,
        )

        results["bm25"][task.task_id] = (
            bm25_full[:TOP_K]
        )
        results["dense"][task.task_id] = (
            dense_full[:TOP_K]
        )
        results["hybrid_rrf"][task.task_id] = [
            document_id
            for document_id, _score
            in hybrid
        ]

    return results


def main() -> None:
    documents = load_documents()
    tasks = load_tasks()
    answerable_tasks = [
        task
        for task in tasks
        if task.should_answer
    ]

    rankings = build_rankings(
        documents,
        tasks,
    )

    scores: list[
        RetrievalStrategyTaskScore
    ] = []

    print(
        "Phase 10 EXP-093 — Fixed Retriever "
        "Comparison and Oracle Routing Ceiling"
    )
    print(
        f"model={MODEL_NAME}"
    )
    print(f"top_k={TOP_K}")
    print(
        f"answerable_tasks={len(answerable_tasks)}"
    )
    print()

    for strategy, retrieved in rankings.items():
        report = evaluate_v2_retrieval(
            tasks=answerable_tasks,
            retrieved_by_task=retrieved,
            k=TOP_K,
        )

        print(strategy)
        print(
            "  mean_supporting_recall="
            f"{report.mean_supporting_recall_at_k:.4f}"
        )
        print(
            "  mean_reciprocal_rank="
            f"{report.mean_reciprocal_rank:.4f}"
        )
        print(
            "  mean_chain_coverage="
            f"{report.mean_evidence_chain_coverage:.4f}"
        )

        for task_report in report.task_reports:
            print(task_report.task_id)
            print(
                "    retrieved="
                f"{retrieved[task_report.task_id]}"
            )
            print(
                "    supporting_recall="
                f"{task_report.supporting_recall_at_k:.4f}"
            )
            print(
                "    reciprocal_rank="
                f"{task_report.reciprocal_rank:.4f}"
            )

            scores.append(
                RetrievalStrategyTaskScore(
                    strategy=strategy,
                    task_id=task_report.task_id,
                    supporting_recall=(
                        task_report.supporting_recall_at_k
                    ),
                    reciprocal_rank=(
                        task_report.reciprocal_rank
                    ),
                    evidence_chain_coverage=(
                        task_report.evidence_chain_coverage
                    ),
                )
            )

        print()

    oracle = evaluate_routing_oracle(
        scores
    )

    print("Oracle routing ceiling")
    for comparison in oracle.comparisons:
        print(comparison.task_id)
        print(
            "  best_strategies="
            f"{list(comparison.best_strategies)}"
        )
        print(
            "  best_supporting_recall="
            f"{comparison.best_supporting_recall:.4f}"
        )
        print(
            "  best_reciprocal_rank="
            f"{comparison.best_reciprocal_rank:.4f}"
        )

    print("Aggregate oracle")
    print(
        "  mean_oracle_supporting_recall="
        f"{oracle.mean_oracle_supporting_recall:.4f}"
    )
    print(
        "  mean_oracle_reciprocal_rank="
        f"{oracle.mean_oracle_reciprocal_rank:.4f}"
    )
    print(
        "  unique_winner_counts="
        f"{oracle.unique_winner_counts}"
    )
    print(
        f"  tied_tasks={oracle.tied_tasks}"
    )


if __name__ == "__main__":
    main()
