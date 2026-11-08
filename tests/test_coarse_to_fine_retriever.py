import pytest

from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)
from knowledge_engine.retrieval.coarse_to_fine import (
    CoarseToFineHierarchicalRetriever,
    HierarchicalRetrievalConfig,
)


class FakeEmbeddingModel:
    def encode(self, values):
        if isinstance(values, str):
            return [1.0, 0.0]

        return [
            [1.0, 0.0]
            for _ in values
        ]


class FakeCrossEncoder:
    def predict(self, pairs):
        scores = []

        for _query, candidate in pairs:
            if "ANSWER-42" in candidate:
                scores.append(10.0)
            elif "middle clue" in candidate:
                scores.append(9.0)
            elif "Target Section" in candidate:
                scores.append(8.0)
            else:
                scores.append(0.0)

        return scores


def build_documents() -> list[StructuredDocument]:
    return [
        StructuredDocument(
            document_id="manual",
            metadata={"title": "Manual"},
            sections=[
                DocumentSection(
                    title="Target Section",
                    text=(
                        "zero one two three four five six "
                        "middle clue ten eleven twelve "
                        "ANSWER-42 fifteen sixteen seventeen"
                    ),
                ),
                DocumentSection(
                    title="Other",
                    text="unrelated material lives here",
                ),
            ],
        )
    ]


def test_config_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        HierarchicalRetrievalConfig(
            chunk_size_words=5,
            chunk_overlap_words=5,
        )


def test_search_returns_radius_window_with_provenance() -> None:
    retriever = CoarseToFineHierarchicalRetriever(
        documents=build_documents(),
        embedding_model_name="unused",
        cross_encoder_model_name="unused",
        config=HierarchicalRetrievalConfig(
            parent_beam=1,
            section_beam=1,
            chunk_size_words=6,
            chunk_overlap_words=2,
            chunk_radius=1,
        ),
        embedding_model=FakeEmbeddingModel(),
        cross_encoder=FakeCrossEncoder(),
    )

    result = retriever.search(
        "What is the answer?"
    )

    assert result.selected_parent_ids == ["manual"]
    assert len(result.windows) == 1

    window = result.windows[0]

    assert window.document_id == "manual"
    assert window.section_title == "Target Section"
    assert "ANSWER-42" in window.text
    assert window.start_word <= window.end_word
    assert result.metadata["chunk_candidates_scored"] > 0


def test_search_rejects_blank_query() -> None:
    retriever = CoarseToFineHierarchicalRetriever(
        documents=build_documents(),
        embedding_model_name="unused",
        cross_encoder_model_name="unused",
        embedding_model=FakeEmbeddingModel(),
        cross_encoder=FakeCrossEncoder(),
    )

    with pytest.raises(ValueError):
        retriever.search("   ")
