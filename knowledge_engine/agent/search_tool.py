from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.vector_math import (
    cosine_similarity,
)
from knowledgebench.documents.schema import KnowledgeDocument


class DenseSearchTool:
    """Thin search-tool wrapper around the Phase 3 dense retriever."""

    def __init__(
        self,
        documents: list[KnowledgeDocument],
        model_name: str,
        model: SentenceTransformer | None = None,
    ) -> None:
        self.documents = documents
        self.model = (
            model
            if model is not None
            else SentenceTransformer(model_name)
        )
        self.document_embeddings = self.model.encode(
            [document.text for document in documents]
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[tuple[str, float]]:
        query_embedding = self.model.encode(
            query
        ).tolist()

        scored = [
            (
                document.document_id,
                cosine_similarity(
                    query_embedding,
                    embedding.tolist(),
                ),
            )
            for document, embedding in zip(
                self.documents,
                self.document_embeddings,
            )
        ]

        scored.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return scored[:top_k]
