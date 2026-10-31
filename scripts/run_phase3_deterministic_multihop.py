import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.metrics.multihop import (
    exact_chain_match,
    hop_accuracy,
)
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)
from scripts.cosine_similarity_exercise import (
    cosine_similarity,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CORPUS_PATH = Path(
    "data/processed/phase3_multihop_corpus_v0.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase3_multihop_tasks_v0.json"
)


def retrieve_top1(
    query: str,
    documents,
    document_embeddings,
    model: SentenceTransformer,
) -> tuple[str, float]:
    query_embedding = model.encode(query).tolist()

    scored = [
        (
            document.document_id,
            cosine_similarity(
                query_embedding,
                embedding.tolist(),
            ),
        )
        for document, embedding in zip(
            documents,
            document_embeddings,
        )
    ]

    scored.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return scored[0]


def main() -> None:
    documents = load_documents_jsonl(CORPUS_PATH)
    tasks = load_multihop_tasks_json(TASK_PATH)

    model = SentenceTransformer(MODEL_NAME)

    document_embeddings = model.encode(
        [document.text for document in documents]
    )

    for task in tasks:
        retrieved_chain: list[str] = []
        expected_chain: list[str] = []

        print(task.task_id)
        print(f"question={task.question}")
        print()

        for hop in task.hops:
            retrieved_id, score = retrieve_top1(
                hop.query,
                documents,
                document_embeddings,
                model,
            )

            retrieved_chain.append(retrieved_id)
            expected_chain.append(
                hop.expected_document_id
            )

            status = (
                "CORRECT"
                if retrieved_id == hop.expected_document_id
                else "WRONG"
            )

            print(
                f"hop={hop.hop_index + 1} "
                f"query={hop.query}"
            )
            print(
                f"  expected={hop.expected_document_id}"
            )
            print(
                f"  retrieved={retrieved_id}"
            )
            print(
                f"  score={score:.6f} "
                f"status={status}"
            )
            print(
                f"  expected_fact={hop.expected_fact}"
            )
            print()

        print(
            f"retrieved_chain={retrieved_chain}"
        )
        print(
            f"expected_chain={expected_chain}"
        )
        print(
            "HopAccuracy="
            f"{hop_accuracy(retrieved_chain, expected_chain):.4f}"
        )
        print(
            "ExactChainMatch="
            f"{exact_chain_match(retrieved_chain, expected_chain):.4f}"
        )
        print()


if __name__ == "__main__":
    main()
