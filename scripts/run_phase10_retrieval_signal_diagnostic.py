import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.vector_math import (
    cosine_similarity,
)
from knowledge_engine.routing.retrieval_signals import (
    build_retrieval_confidence_signals,
)
from knowledgebench.documents.v2_schema import (
    KnowledgeBenchV2Document,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_documents_v0.json"
)
TASKS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_tasks_v0.json"
)

WINNERS = {
    "kbv2-hard-001": ["dense"],
    "kbv2-hard-002": ["bm25"],
    "kbv2-hard-005": ["bm25"],
    "kbv2-hard-006": [
        "bm25",
        "dense",
        "hybrid_rrf",
    ],
    "kbv2-hard-007": [
        "bm25",
        "dense",
        "hybrid_rrf",
    ],
    "kbv2-hard-010": [
        "dense",
        "hybrid_rrf",
    ],
}


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


def main() -> None:
    documents = load_documents()
    tasks = [
        task
        for task in load_tasks()
        if task.should_answer
    ]

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

    print(
        "Phase 10 EXP-095 — Retrieval Confidence "
        "Signal Diagnostic"
    )
    print(f"model={MODEL_NAME}")
    print()

    for task in tasks:
        bm25_ranked = bm25.rank(
            task.question,
            top_k=len(documents),
        )

        query_embedding = model.encode(
            task.question
        ).tolist()

        dense_ranked = [
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
        dense_ranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        signals = build_retrieval_confidence_signals(
            bm25_ranked=bm25_ranked,
            dense_ranked=dense_ranked,
        )

        print(task.task_id)
        print(
            f"  winners={WINNERS[task.task_id]}"
        )
        print(
            "  bm25_top1="
            f"{bm25_ranked[0][0]}"
        )
        print(
            "  bm25_top1_score="
            f"{signals.bm25_top1_score:.4f}"
        )
        print(
            "  bm25_margin="
            f"{signals.bm25_margin:.4f}"
        )
        print(
            "  bm25_nonzero_count="
            f"{signals.bm25_nonzero_count}"
        )
        print(
            "  dense_top1="
            f"{dense_ranked[0][0]}"
        )
        print(
            "  dense_top1_score="
            f"{signals.dense_top1_score:.4f}"
        )
        print(
            "  dense_margin="
            f"{signals.dense_margin:.4f}"
        )
        print(
            "  top1_agreement="
            f"{signals.top1_agreement}"
        )
        print(
            "  top3_overlap_count="
            f"{signals.top3_overlap_count}"
        )
        print(
            "  top3_jaccard="
            f"{signals.top3_jaccard:.4f}"
        )
        print()


if __name__ == "__main__":
    main()
