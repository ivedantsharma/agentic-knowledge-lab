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
from knowledgebench.tasks.query_transformation_schema import (
    OracleQueryTransformation,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SINGLE_SHOT_K = 5
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

    def hybrid_rank(
        query: str,
        top_k: int,
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
                top_k=top_k,
            )
        ]

    single_recalls = []
    transformed_recalls = []
    single_budgets = []
    transformed_budgets = []

    print(
        "Phase 10 EXP-099 — Oracle Query "
        "Transformation Upper Bound"
    )
    print(
        f"single_shot_k={SINGLE_SHOT_K}"
    )
    print(
        f"per_transformed_query_k={PER_QUERY_K}"
    )
    print()

    for task in transformations:
        single = hybrid_rank(
            task.original_question,
            top_k=SINGLE_SHOT_K,
        )

        transformed = []
        per_query_results = []

        for query in task.transformed_queries:
            ranked = hybrid_rank(
                query,
                top_k=PER_QUERY_K,
            )
            per_query_results.append(
                (query, ranked)
            )
            for document_id in ranked:
                if document_id not in transformed:
                    transformed.append(document_id)

        single_recall = recall(
            single,
            task.supporting_document_ids,
        )
        transformed_recall = recall(
            transformed,
            task.supporting_document_ids,
        )

        single_recalls.append(single_recall)
        transformed_recalls.append(
            transformed_recall
        )
        single_budgets.append(
            len(single)
        )
        transformed_budgets.append(
            sum(
                len(ids)
                for _query, ids
                in per_query_results
            )
        )

        print(task.task_id)
        print(
            f"  supporting={sorted(task.supporting_document_ids)}"
        )
        print(
            f"  single_shot={single}"
        )
        print(
            "  single_shot_recall="
            f"{single_recall:.4f}"
        )

        for query, ids in per_query_results:
            print(
                f"  transformed_query={query!r}"
            )
            print(
                f"    retrieved={ids}"
            )

        print(
            f"  transformed_union={transformed}"
        )
        print(
            "  transformed_recall="
            f"{transformed_recall:.4f}"
        )
        print(
            "  single_budget="
            f"{len(single)}"
        )
        print(
            "  transformed_budget="
            f"{transformed_budgets[-1]}"
        )
        print()

    print("Aggregate")
    print(
        "  single_shot_mean_recall="
        f"{sum(single_recalls) / len(single_recalls):.4f}"
    )
    print(
        "  transformed_mean_recall="
        f"{sum(transformed_recalls) / len(transformed_recalls):.4f}"
    )
    print(
        "  mean_single_budget="
        f"{sum(single_budgets) / len(single_budgets):.4f}"
    )
    print(
        "  mean_transformed_budget="
        f"{sum(transformed_budgets) / len(transformed_budgets):.4f}"
    )


if __name__ == "__main__":
    main()
