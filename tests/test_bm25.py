import pytest

from knowledge_engine.retrieval.bm25 import BM25Retriever, tokenize


def test_tokenize_preserves_technical_identifier() -> None:
    assert tokenize("ERR_CONNECTION_REFUSED!") == ["err_connection_refused"]


def test_bm25_ranks_exact_match_first() -> None:
    retriever = BM25Retriever(
        document_ids=["python", "http", "finance"],
        document_texts=[
            "Python virtual environments isolate dependencies.",
            "ERR_CONNECTION_REFUSED means the server refused the connection.",
            "Stock markets rose today.",
        ],
    )

    results = retriever.rank("ERR_CONNECTION_REFUSED", top_k=3)

    assert results[0][0] == "http"
    assert results[0][1] > results[1][1]


def test_bm25_returns_requested_top_k() -> None:
    retriever = BM25Retriever(
        document_ids=["a", "b", "c"],
        document_texts=["alpha", "beta", "gamma"],
    )

    results = retriever.rank("alpha", top_k=2)

    assert len(results) == 2


def test_bm25_zero_top_k_returns_empty_list() -> None:
    retriever = BM25Retriever(
        document_ids=["a"],
        document_texts=["alpha"],
    )

    assert retriever.rank("alpha", top_k=0) == []


def test_bm25_rejects_mismatched_inputs() -> None:
    with pytest.raises(ValueError):
        BM25Retriever(
            document_ids=["a"],
            document_texts=["A", "B"],
        )
