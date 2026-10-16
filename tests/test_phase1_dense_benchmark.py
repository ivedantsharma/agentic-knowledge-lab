from knowledgebench.documents.schema import KnowledgeDocument
from scripts.run_phase1_dense_benchmark import rank_documents


class FakeEmbedding:
    def __init__(self, values: list[float]) -> None:
        self._values = values

    def tolist(self) -> list[float]:
        return self._values


class FakeModel:
    def encode(self, text: str) -> FakeEmbedding:
        assert text == "query"
        return FakeEmbedding([1.0, 0.0])


def test_rank_documents_orders_by_similarity() -> None:
    document_ids = ["a", "b", "c"]
    document_texts = ["A", "B", "C"]
    document_embeddings = [
        FakeEmbedding([1.0, 0.0]),
        FakeEmbedding([0.8, 0.2]),
        FakeEmbedding([0.0, 1.0]),
    ]

    ranked = rank_documents(
        query="query",
        document_ids=document_ids,
        document_texts=document_texts,
        document_embeddings=document_embeddings,
        model=FakeModel(),  # type: ignore[arg-type]
        top_k=2,
    )

    assert ranked == ["a", "b"]
