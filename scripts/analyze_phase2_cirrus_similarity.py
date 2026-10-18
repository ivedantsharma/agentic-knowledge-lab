import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.rich_context_chunker import (
    chunk_by_rich_context,
)
from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)
from scripts.cosine_similarity_exercise import cosine_similarity

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

STRUCTURED_PATH = Path(
    "data/processed/phase2_structured_documents_context_v1.json"
)

QUERY = "Where are Cirrus jobs sent after exhausting all retries?"

def main() -> None:
    documents = load_structured_documents_json(
        STRUCTURED_PATH
    )

    cirrus = next(
        document
        for document in documents
        if document.document_id == "manual_gamma"
    )

    chunks = chunk_by_rich_context(cirrus)

    model = SentenceTransformer(MODEL_NAME)

    query_embedding = model.encode(QUERY).tolist()

    scored = []

    for chunk in chunks:
        embedding = model.encode(chunk.text).tolist()

        score = cosine_similarity(
            query_embedding,
            embedding,
        )

        scored.append(
            (
                score,
                chunk.chunk_id,
                chunk.text,
            )
        )

    scored.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    print("Cirrus similarity analysis")
    print(f"Query: {QUERY}")
    print()

    for rank, (score, chunk_id, text) in enumerate(
        scored,
        start=1,
    ):
        print(
            f"rank={rank} "
            f"score={score:.6f} "
            f"id={chunk_id}"
        )
        print(text)
        print()


if __name__ == "__main__":
    main()
