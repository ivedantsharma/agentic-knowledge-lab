"""Shared ranking adapters for integrated BM25, dense and hybrid retrieval.

Dense/Hybrid require an explicit encoder or load frozen MiniLM on demand.
The default BM25 backend has no model download or GPU dependency at runtime.
"""

from typing import Protocol

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.hybrid import reciprocal_rank_fusion
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class RankingBackend(Protocol):
    def rank(self, query: str, top_k: int) -> list[tuple[str, float]]: ...


class _Encoder(Protocol):
    def encode(self, values): ...


class DenseRankingBackend:
    def __init__(self, documents: list[KnowledgeBenchV2Document], encoder: _Encoder):
        self.ids = [doc.document_id for doc in documents]
        self.encoder = encoder
        self.embeddings = encoder.encode([doc.text for doc in documents])

    def rank(self, query: str, top_k: int) -> list[tuple[str, float]]:
        vector = self.encoder.encode(query).tolist()
        scored = [
            (doc_id, cosine_similarity(vector, embedding.tolist()))
            for doc_id, embedding in zip(self.ids, self.embeddings)
        ]
        return sorted(scored, key=lambda hit: (-hit[1], hit[0]))[:top_k]


class HybridRankingBackend:
    def __init__(self, bm25: BM25Retriever, dense: DenseRankingBackend):
        self.bm25 = bm25
        self.dense = dense
        self.size = len(dense.ids)

    def rank(self, query: str, top_k: int) -> list[tuple[str, float]]:
        lexical = [doc_id for doc_id, _ in self.bm25.rank(query, self.size)]
        semantic = [doc_id for doc_id, _ in self.dense.rank(query, self.size)]
        return reciprocal_rank_fusion([lexical, semantic], top_k=top_k, rrf_k=60)


def create_ranking_backend(
    documents: list[KnowledgeBenchV2Document],
    *,
    name: str = "bm25",
    encoder: _Encoder | None = None,
) -> RankingBackend:
    if not documents or len({doc.document_id for doc in documents}) != len(documents):
        raise ValueError("documents must be nonempty with unique IDs")
    if name not in {"bm25", "dense", "hybrid"}:
        raise ValueError("unknown backend: choose bm25, dense or hybrid")
    lexical = BM25Retriever(
        document_ids=[doc.document_id for doc in documents],
        document_texts=[doc.text for doc in documents],
    )
    if name == "bm25":
        return lexical
    if encoder is None:
        from sentence_transformers import SentenceTransformer

        encoder = SentenceTransformer(MODEL_NAME)
    dense = DenseRankingBackend(documents, encoder)
    if name == "dense":
        return dense
    return HybridRankingBackend(lexical, dense)
