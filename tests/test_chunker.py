import pytest

from knowledge_engine.ingestion.chunker import chunk_by_words
from knowledge_engine.ingestion.schema import SourceDocument


def test_chunk_by_words_without_overlap() -> None:
    document = SourceDocument(
        document_id="doc-1",
        text="one two three four five six seven eight",
    )

    chunks = chunk_by_words(
        document,
        chunk_size_words=3,
        overlap_words=0,
    )

    assert [chunk.text for chunk in chunks] == [
        "one two three",
        "four five six",
        "seven eight",
    ]

    assert chunks[0].chunk_id == "doc-1::chunk-0000"
    assert chunks[0].start_word == 0
    assert chunks[0].end_word == 3
    assert chunks[2].start_word == 6
    assert chunks[2].end_word == 8


def test_chunk_by_words_with_overlap() -> None:
    document = SourceDocument(
        document_id="doc-1",
        text="one two three four five six seven",
    )

    chunks = chunk_by_words(
        document,
        chunk_size_words=4,
        overlap_words=2,
    )

    assert [chunk.text for chunk in chunks] == [
        "one two three four",
        "three four five six",
        "five six seven",
    ]


def test_chunk_metadata_preserves_source_metadata() -> None:
    document = SourceDocument(
        document_id="doc-1",
        text="one two three four",
        metadata={"source": "synthetic", "section": "intro"},
    )

    chunks = chunk_by_words(
        document,
        chunk_size_words=2,
    )

    assert chunks[0].metadata["source"] == "synthetic"
    assert chunks[0].metadata["section"] == "intro"
    assert chunks[0].metadata["chunk_size_words"] == 2


@pytest.mark.parametrize(
    ("chunk_size_words", "overlap_words"),
    [
        (0, 0),
        (-1, 0),
        (3, -1),
        (3, 3),
        (3, 4),
    ],
)
def test_invalid_chunk_configuration_is_rejected(
    chunk_size_words: int,
    overlap_words: int,
) -> None:
    document = SourceDocument(
        document_id="doc-1",
        text="one two three",
    )

    with pytest.raises(ValueError):
        chunk_by_words(
            document,
            chunk_size_words=chunk_size_words,
            overlap_words=overlap_words,
        )
