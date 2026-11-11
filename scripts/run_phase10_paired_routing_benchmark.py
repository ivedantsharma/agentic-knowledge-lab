import json
import sys
from collections import defaultdict
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


def reciprocal_rank(
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


def recall_at_k(
    retrieved: list[str],
    supporting: set[str],
) -> float:
    return (
        len(set(retrieved) & supporting)
        / len(supporting)
    )


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

    style_metrics = defaultdict(
        lambda: defaultdict(list)
    )
    pair_winners = defaultdict(dict)
    strategy_metrics = defaultdict(list)

    print(
        "Phase 10 EXP-096 — Paired Lexical vs "
        "Semantic Routing Benchmark"
    )
    print(f"model={MODEL_NAME}")
    print(f"top_k={TOP_K}")
    print(f"tasks={len(tasks)}")
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

        task_scores = {}

        print(task.task_id)
        print(f"  pair_id={task.pair_id}")
        print(
            f"  query_style={task.query_style.value}"
        )
        print(f"  question={task.question!r}")

        for strategy, retrieved in rankings.items():
            recall = recall_at_k(
                retrieved,
                task.supporting_document_ids,
            )
            rr = reciprocal_rank(
                retrieved,
                task.supporting_document_ids,
            )
            task_scores[strategy] = (
                recall,
                rr,
            )
            strategy_metrics[strategy].append(
                (recall, rr)
            )
            style_metrics[
                task.query_style.value
            ][strategy].append(
                (recall, rr)
            )

            print(f"  {strategy}")
            print(
                f"    retrieved={retrieved}"
            )
            print(
                f"    recall@3={recall:.4f}"
            )
            print(
                f"    reciprocal_rank={rr:.4f}"
            )

        best_key = max(
            task_scores.values()
        )
        winners = sorted(
            strategy
            for strategy, score
            in task_scores.items()
            if score == best_key
        )
        pair_winners[task.pair_id][
            task.query_style.value
        ] = winners

        print(f"  winners={winners}")
        print()

    print("By query style")
    for style, strategies in style_metrics.items():
        print(style)
        for strategy, values in strategies.items():
            print(
                f"  {strategy}_mean_recall="
                f"{sum(v[0] for v in values) / len(values):.4f}"
            )
            print(
                f"  {strategy}_mrr="
                f"{sum(v[1] for v in values) / len(values):.4f}"
            )

    print()
    print("Overall fixed strategies")
    for strategy, values in strategy_metrics.items():
        print(strategy)
        print(
            "  mean_recall="
            f"{sum(v[0] for v in values) / len(values):.4f}"
        )
        print(
            "  mrr="
            f"{sum(v[1] for v in values) / len(values):.4f}"
        )

    print()
    print("Pair winner shifts")
    shift_count = 0
    for pair_id, styles in pair_winners.items():
        lexical = styles.get(
            "lexical_explicit",
            [],
        )
        semantic = styles.get(
            "semantic_paraphrase",
            [],
        )
        changed = lexical != semantic
        shift_count += int(changed)

        print(pair_id)
        print(f"  lexical={lexical}")
        print(f"  semantic={semantic}")
        print(f"  winner_shift={changed}")

    print()
    print(
        f"winner_shift_pairs={shift_count}"
    )
    print(
        f"total_pairs={len(pair_winners)}"
    )


if __name__ == "__main__":
    main()
