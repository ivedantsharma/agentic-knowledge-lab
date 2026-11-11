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
from knowledgebench.evaluation.ranking_oracle import (
    RankingStrategyScore,
    evaluate_ranking_oracle,
)
from knowledgebench.tasks.routing_schema import (
    RoutingBenchmarkTask,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3

DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_documents_v0.json"
)
TASKS_PATH = Path(
    "data/processed/phase10_routing_pairs_v0.json"
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


def load_tasks() -> list[RoutingBenchmarkTask]:
    return [
        RoutingBenchmarkTask.model_validate(item)
        for item in json.loads(
            TASKS_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def rr(
    retrieved: list[str],
    supporting: set[str],
) -> float:
    for rank, document_id in enumerate(
        retrieved,
        start=1,
    ):
        if document_id in supporting:
            return 1.0 / rank
    return 0.0


def main() -> None:
    documents = load_documents()
    tasks = load_tasks()

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

    scores: list[RankingStrategyScore] = []
    fixed_rr: dict[str, list[float]] = {
        "bm25": [],
        "dense": [],
        "hybrid_rrf": [],
    }

    print(
        "Phase 10 EXP-097 — Paired Benchmark "
        "Routing Value Decomposition"
    )
    print(f"tasks={len(tasks)}")
    print(f"top_k={TOP_K}")
    print()

    for task in tasks:
        bm25_full = bm25.rank(
            task.question,
            top_k=len(documents),
        )
        bm25_ids = [
            document_id
            for document_id, _score
            in bm25_full[:TOP_K]
        ]

        query_embedding = model.encode(
            task.question
        ).tolist()

        dense_full = [
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
        dense_full.sort(
            key=lambda item: item[1],
            reverse=True,
        )
        dense_ids = [
            document_id
            for document_id, _score
            in dense_full[:TOP_K]
        ]

        hybrid_ids = [
            document_id
            for document_id, _score
            in reciprocal_rank_fusion(
                rankings=[
                    [
                        document_id
                        for document_id, _score
                        in bm25_full
                    ],
                    [
                        document_id
                        for document_id, _score
                        in dense_full
                    ],
                ],
                top_k=TOP_K,
            )
        ]

        rankings = {
            "bm25": bm25_ids,
            "dense": dense_ids,
            "hybrid_rrf": hybrid_ids,
        }

        print(task.task_id)
        print(
            f"  style={task.query_style.value}"
        )

        for strategy, retrieved in rankings.items():
            score = rr(
                retrieved,
                task.supporting_document_ids,
            )
            fixed_rr[strategy].append(score)
            scores.append(
                RankingStrategyScore(
                    task_id=task.task_id,
                    strategy=strategy,
                    reciprocal_rank=score,
                )
            )
            print(
                f"  {strategy}_rr={score:.4f}"
            )

        print()

    oracle = evaluate_ranking_oracle(
        scores
    )

    print("Fixed strategy MRR")
    for strategy, values in fixed_rr.items():
        print(
            f"  {strategy}="
            f"{sum(values) / len(values):.4f}"
        )

    best_fixed_strategy = max(
        fixed_rr,
        key=lambda strategy: (
            sum(fixed_rr[strategy])
            / len(fixed_rr[strategy])
        ),
    )
    best_fixed_mrr = (
        sum(fixed_rr[best_fixed_strategy])
        / len(fixed_rr[best_fixed_strategy])
    )

    print()
    print("Oracle")
    print(
        f"  oracle_mrr={oracle.oracle_mrr:.4f}"
    )
    print(
        "  best_fixed_strategy="
        f"{best_fixed_strategy}"
    )
    print(
        f"  best_fixed_mrr={best_fixed_mrr:.4f}"
    )
    print(
        "  absolute_headroom="
        f"{oracle.oracle_mrr - best_fixed_mrr:.4f}"
    )
    print(
        "  relative_headroom="
        f"{(oracle.oracle_mrr - best_fixed_mrr) / best_fixed_mrr:.4f}"
    )
    print(
        "  unique_winner_counts="
        f"{oracle.unique_winner_counts}"
    )
    print(
        f"  tied_tasks={oracle.tied_tasks}"
    )

    print()
    print("Per-task oracle")
    for report in oracle.task_reports:
        print(report.task_id)
        print(
            "  best_rr="
            f"{report.best_reciprocal_rank:.4f}"
        )
        print(
            "  best_strategies="
            f"{list(report.best_strategies)}"
        )


if __name__ == "__main__":
    main()
