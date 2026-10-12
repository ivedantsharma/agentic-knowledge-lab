from cosine_similarity_exercise import cosine_similarity
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main() -> None:
    sentences = {
        "S1": "A dog is sleeping on the couch.",
        "S2": "A puppy is taking a nap on the sofa.",
        "S3": "The stock market increased today.",
        "S4": "Investors saw equity prices rise during trading.",
    }

    model = SentenceTransformer(MODEL_NAME)

    labels = list(sentences.keys())
    texts = [sentences[label] for label in labels]

    embeddings = model.encode(texts)

    print("Model:", MODEL_NAME)
    print("Embedding dimension:", len(embeddings[0]))
    print()

    pairs = [
        ("S1", "S2"),
        ("S1", "S3"),
        ("S3", "S4"),
    ]

    embedding_by_label = {
        label: embedding.tolist()
        for label, embedding in zip(labels, embeddings)
    }

    for left, right in pairs:
        score = cosine_similarity(
            embedding_by_label[left],
            embedding_by_label[right],
        )
        print(f"{left} vs {right}: {score:.4f}")


if __name__ == "__main__":
    main()
