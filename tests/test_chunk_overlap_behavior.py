from knowledge_engine.ingestion.chunker import chunk_by_words
from knowledge_engine.ingestion.schema import SourceDocument


def test_overlap_preserves_boundary_context() -> None:
    document = SourceDocument(
        document_id="doc",
        text=(
            "a b c d e f g h i j "
            "context answer k l m n o p q r"
        ),
    )

    without_overlap = chunk_by_words(
        document,
        chunk_size_words=10,
        overlap_words=0,
    )

    with_overlap = chunk_by_words(
        document,
        chunk_size_words=10,
        overlap_words=3,
    )

    assert "context answer" not in without_overlap[0].text
    assert "context answer" in without_overlap[1].text

    overlapping_texts = [chunk.text for chunk in with_overlap]
    assert any(
        "i j context answer" in text
        for text in overlapping_texts
    )
