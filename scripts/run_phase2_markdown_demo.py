from pathlib import Path

from sentence_transformers import CrossEncoder, SentenceTransformer

from knowledge_engine.ingestion.markdown_parser import (
    parse_markdown_document,
)
from knowledge_engine.ingestion.structure_chunker import (
    chunk_by_section,
)
from knowledge_engine.retrieval.reranker import (
    sort_by_reranker_scores,
)
from scripts.cosine_similarity_exercise import (
    cosine_similarity,
)


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

MARKDOWN_PATH = Path(
    "data/raw/phase2_atlas_manual.md"
)

QUERY = "What is the current Atlas signing-key identifier?"


def main() -> None:
    document = parse_markdown_document(
        MARKDOWN_PATH,
        document_id="atlas_markdown",
    )

    chunks = chunk_by_section(document)

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )
    reranker = CrossEncoder(
        RERANKER_MODEL
    )

    chunk_ids = [chunk.chunk_id for chunk in chunks]
    chunk_texts = [chunk.text for chunk in chunks]
    embeddings = embedding_model.encode(chunk_texts)

    query_embedding = embedding_model.encode(
        QUERY
    ).tolist()

    scored = [
        (
            chunk_id,
            cosine_similarity(
                query_embedding,
                embedding.tolist(),
            ),
        )
        for chunk_id, embedding in zip(
            chunk_ids,
            embeddings,
        )
    ]

    scored.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    dense_top3 = [
        chunk_id
        for chunk_id, _ in scored[:3]
    ]

    chunk_by_id = {
        chunk.chunk_id: chunk
        for chunk in chunks
    }

    reranker_scores = reranker.predict(
        [
            (
                QUERY,
                chunk_by_id[chunk_id].text,
            )
            for chunk_id in dense_top3
        ]
    ).tolist()

    reranked = sort_by_reranker_scores(
        dense_top3,
        reranker_scores,
    )

    print("Markdown ingestion demo")
    print(f"document_id={document.document_id}")
    print(f"title={document.metadata['title']}")
    print(
        "sections="
        f"{[section.title for section in document.sections]}"
    )
    print()

    print(f"query={QUERY}")
    print(f"dense_top3={dense_top3}")
    print(
        "reranker_scores="
        f"{[round(score, 6) for score in reranker_scores]}"
    )
    print(f"reranked={reranked}")
    print()

    for chunk_id in reranked:
        print(chunk_id)
        print(chunk_by_id[chunk_id].text)
        print()


if __name__ == "__main__":
    main()
