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
from knowledgebench.evaluation.budget_oracle import (
    evaluate_budget_oracle,
    minimal_k_for_max_recall,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CANDIDATE_KS = (1, 2, 3, 5)

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

    budget_results = []

    print(
        "Phase 10 EXP-098 — Adaptive Top-K "
        "Budget Oracle"
    )
    print(f"candidate_ks={CANDIDATE_KS}")
    print()

    for task in tasks:
        bm25_full = bm25.rank(
            task.question,
            top_k=len(documents),
        )

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

        hybrid_full = [
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

        result = minimal_k_for_max_recall(
            task_id=task.task_id,
            ranked_ids=hybrid_full,
            supporting_ids=(
                task.supporting_document_ids
            ),
            candidate_ks=CANDIDATE_KS,
        )
        budget_results.append(result)

        print(task.task_id)
        print(
            "  supporting_docs="
            f"{len(task.supporting_document_ids)}"
        )
        print(
            "  minimal_k_for_max_recall="
            f"{result.minimal_k_for_max_recall}"
        )
        print(
            f"  max_recall={result.max_recall:.4f}"
        )

        for k in CANDIDATE_KS:
            print(
                f"  recall@{k}="
                f"{result.recall_by_k[k]:.4f}"
            )

        print()

    oracle = evaluate_budget_oracle(
        budget_results
    )

    print("Budget oracle")
    print(
        "  mean_minimal_k="
        f"{oracle.mean_minimal_k:.4f}"
    )
    print(
        "  max_required_k="
        f"{oracle.max_required_k}"
    )

    for fixed_k in CANDIDATE_KS:
        mean_recall = (
            sum(
                result.recall_by_k[fixed_k]
                for result in budget_results
            )
            / len(budget_results)
        )
        print(
            f"  fixed_k={fixed_k} "
            f"mean_recall={mean_recall:.4f}"
        )


if __name__ == "__main__":
    main()
