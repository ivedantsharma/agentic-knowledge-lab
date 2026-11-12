import json
import sys
from collections import Counter, defaultdict
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
from knowledge_engine.training.policy_labeler import (
    label_budget_policy,
)
from knowledgebench.documents.v2_schema import (
    KnowledgeBenchV2Document,
)
from knowledgebench.tasks.routing_schema import (
    RoutingBenchmarkTask,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_documents_v0.json"
)
ROUTING_PATH = Path(
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
            ROUTING_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


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

    def hybrid_full_rank(
        query: str,
    ) -> list[str]:
        bm25_full = bm25.rank(
            query,
            top_k=len(documents),
        )

        query_embedding = model.encode(
            query
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

        return [
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
                top_k=len(documents),
            )
        ]

    labels_by_pair = defaultdict(list)
    action_counts: Counter[str] = Counter()

    print(
        "Phase 11 EXP-107 — Existing-Corpus "
        "Oracle Policy Label Mining"
    )
    print()

    for task in tasks:
        ranked_ids = hybrid_full_rank(
            task.question
        )
        label = label_budget_policy(
            ranked_ids=ranked_ids,
            supporting_ids=(
                task.supporting_document_ids
            ),
        )

        labels_by_pair[
            task.pair_id
        ].append(
            (
                task.task_id,
                task.query_style.value,
                label.action.value,
                label.minimal_k,
            )
        )
        action_counts[
            label.action.value
        ] += 1

        print(task.task_id)
        print(
            f"  pair_id={task.pair_id}"
        )
        print(
            f"  style={task.query_style.value}"
        )
        print(
            f"  action={label.action.value}"
        )
        print(
            f"  minimal_k={label.minimal_k}"
        )
        print(
            f"  max_recall={label.max_recall:.4f}"
        )
        print(
            f"  recall_by_k={label.recall_by_k}"
        )
        print()

    stable_pairs = 0
    unstable_pairs = 0

    print("Pair stability")

    for pair_id, rows in sorted(
        labels_by_pair.items()
    ):
        actions = {
            row[2]
            for row in rows
        }
        stable = len(actions) == 1

        stable_pairs += int(stable)
        unstable_pairs += int(
            not stable
        )

        print(pair_id)
        print(f"  rows={rows}")
        print(
            f"  action_stable={stable}"
        )

    print()
    print("Summary")
    print(
        f"action_counts={dict(action_counts)}"
    )
    print(
        f"stable_pairs={stable_pairs}"
    )
    print(
        f"unstable_pairs={unstable_pairs}"
    )


if __name__ == "__main__":
    main()
