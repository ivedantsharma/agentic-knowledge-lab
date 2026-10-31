import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledgebench.documents.loader import load_documents_jsonl
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


def main() -> None:
    documents = load_documents_jsonl(CORPUS_PATH)
    tasks = load_multihop_tasks_json(TASK_PATH)

    model = SentenceTransformer(MODEL_NAME)

    document_embeddings = model.encode(
        [document.text for document in documents]
    )

    for task in tasks:
        query_embedding = model.encode(
            task.question
        ).tolist()

        scored = [
            (
                document.document_id,
                cosine_similarity(
                    query_embedding,
                    embedding.tolist(),
                ),
                document.text,
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

        expected_chain = [
            hop.expected_document_id
            for hop in task.hops
        ]

        print(task.task_id)
        print(f"question={task.question}")
        print(f"expected_chain={expected_chain}")
        print()

        for rank, (
            document_id,
            score,
            text,
        ) in enumerate(scored, start=1):
            marker = (
                "EXPECTED"
                if document_id in expected_chain
                else "DISTRACTOR"
            )
            print(
                f"rank={rank} "
                f"score={score:.6f} "
                f"{marker} "
                f"id={document_id}"
            )
            print(text)
            print()


if __name__ == "__main__":
    main()
