from sentence_transformers import SentenceTransformer

from scripts.cosine_similarity_exercise import cosine_similarity


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DOCUMENTS = {
    "doc_python": (
        "Python virtual environments isolate project dependencies so different "
        "projects can use different package versions."
    ),
    "doc_dog": "A puppy slept peacefully on the sofa after playing outside.",
    "doc_finance": (
        "Stock prices rose during the trading session as investors became more optimistic."
    ),
    "doc_rl": (
        "Reinforcement learning trains an agent using rewards that encourage useful behavior."
    ),
    "doc_http": (
        "ERR_CONNECTION_REFUSED usually means the target server rejected or did not accept "
        "the network connection."
    ),
}


def rank_documents(
    query: str,
    documents: dict[str, str],
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[tuple[str, float]]:
    """Return document IDs ranked by semantic similarity to the query."""
    # TODO 1: encode the query.
    # TODO 2: encode all document texts.
    # TODO 3: calculate cosine similarity for each document.
    # TODO 4: sort from highest score to lowest.
    # TODO 5: return only the first top_k results.
    raise NotImplementedError


def main() -> None:
    model = SentenceTransformer(MODEL_NAME)

    query = "How do I stop Python package versions from conflicting between projects?"

    results = rank_documents(
        query=query,
        documents=DOCUMENTS,
        model=model,
        top_k=3,
    )

    print("Query:", query)
    print()

    for rank, (document_id, score) in enumerate(results, start=1):
        print(f"{rank}. {document_id}: {score:.4f}")
        print(f"   {DOCUMENTS[document_id]}")


if __name__ == "__main__":
    main()
