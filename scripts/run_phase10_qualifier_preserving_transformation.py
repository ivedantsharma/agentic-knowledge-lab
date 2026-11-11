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
from knowledge_engine.routing.qualifier_preserving_queries import (
    build_qualifier_preserving_queries,
)
from knowledgebench.documents.v2_schema import (
    KnowledgeBenchV2Document,
)
from knowledgebench.tasks.query_transformation_schema import (
    OracleQueryTransformation,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
PER_QUERY_K = 1

DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_documents_v0.json"
)
TRANSFORMATIONS_PATH = Path(
    "data/processed/phase10_oracle_query_transformations_v0.json"
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


def load_transformations() -> list[OracleQueryTransformation]:
    return [
        OracleQueryTransformation.model_validate(item)
        for item in json.loads(
            TRANSFORMATIONS_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def recall(
    retrieved: list[str],
    supporting: set[str],
) -> float:
    return (
        len(set(retrieved) & supporting)
        / len(supporting)
    )


def main() -> None:
    documents = load_documents()
    transformations = load_transformations()

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

    def hybrid_rank(query: str) -> list[str]:
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
                top_k=PER_QUERY_K,
            )
        ]

    baseline_recalls = []
    preserved_recalls = []

    print(
        "Phase 10 EXP-100 — Qualifier-Preserving "
        "Query Transformation"
    )
    print(f"per_query_k={PER_QUERY_K}")
    print()

    for task in transformations:
        baseline_union: list[str] = []
        for query in task.transformed_queries:
            for document_id in hybrid_rank(query):
                if document_id not in baseline_union:
                    baseline_union.append(document_id)

        preserved = build_qualifier_preserving_queries(
            task.task_id
        )

        preserved_union: list[str] = []
        preserved_per_query = []

        for query in preserved.transformed_queries:
            ids = hybrid_rank(query)
            preserved_per_query.append(
                (query, ids)
            )
            for document_id in ids:
                if document_id not in preserved_union:
                    preserved_union.append(document_id)

        baseline_recall = recall(
            baseline_union,
            task.supporting_document_ids,
        )
        preserved_recall = recall(
            preserved_union,
            task.supporting_document_ids,
        )

        baseline_recalls.append(
            baseline_recall
        )
        preserved_recalls.append(
            preserved_recall
        )

        print(task.task_id)
        print(
            f"  baseline_union={baseline_union}"
        )
        print(
            "  baseline_recall="
            f"{baseline_recall:.4f}"
        )

        for query, ids in preserved_per_query:
            print(
                f"  preserved_query={query!r}"
            )
            print(
                f"    retrieved={ids}"
            )

        print(
            f"  preserved_union={preserved_union}"
        )
        print(
            "  preserved_recall="
            f"{preserved_recall:.4f}"
        )
        print()

    print("Aggregate")
    print(
        "  baseline_mean_recall="
        f"{sum(baseline_recalls) / len(baseline_recalls):.4f}"
    )
    print(
        "  qualifier_preserved_mean_recall="
        f"{sum(preserved_recalls) / len(preserved_recalls):.4f}"
    )


if __name__ == "__main__":
    main()
