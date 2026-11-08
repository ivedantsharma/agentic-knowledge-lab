from dataclasses import dataclass
from typing import Any

from sentence_transformers import CrossEncoder, SentenceTransformer

from knowledge_engine.ingestion.hierarchical_chunker import chunk_section
from knowledge_engine.ingestion.structured_schema import StructuredDocument
from knowledge_engine.retrieval.hierarchical import (
    HierarchicalDenseRetriever,
    render_section,
)


@dataclass(frozen=True)
class HierarchicalRetrievalConfig:
    parent_beam: int = 2
    section_beam: int = 2
    chunk_size_words: int = 10
    chunk_overlap_words: int = 3
    chunk_radius: int = 1

    def __post_init__(self) -> None:
        if self.parent_beam <= 0:
            raise ValueError("parent_beam must be greater than zero")
        if self.section_beam <= 0:
            raise ValueError("section_beam must be greater than zero")
        if self.chunk_size_words <= 0:
            raise ValueError("chunk_size_words must be greater than zero")
        if self.chunk_overlap_words < 0:
            raise ValueError("chunk_overlap_words must be zero or greater")
        if self.chunk_overlap_words >= self.chunk_size_words:
            raise ValueError(
                "chunk_overlap_words must be smaller than chunk_size_words"
            )
        if self.chunk_radius < 0:
            raise ValueError("chunk_radius must be zero or greater")


@dataclass(frozen=True)
class HierarchicalEvidenceWindow:
    document_id: str
    section_index: int
    section_title: str
    section_score: float
    anchor_chunk_index: int
    anchor_chunk_score: float
    start_word: int
    end_word: int
    text: str


@dataclass(frozen=True)
class HierarchicalRetrievalResult:
    query: str
    selected_parent_ids: list[str]
    windows: list[HierarchicalEvidenceWindow]
    metadata: dict[str, Any]


class CoarseToFineHierarchicalRetriever:
    """Reusable document → section → chunk retrieval pipeline."""

    def __init__(
        self,
        documents: list[StructuredDocument],
        embedding_model_name: str,
        cross_encoder_model_name: str,
        config: HierarchicalRetrievalConfig | None = None,
        embedding_model: SentenceTransformer | None = None,
        cross_encoder: CrossEncoder | None = None,
    ) -> None:
        if not documents:
            raise ValueError("hierarchical retriever requires documents")

        self.documents = documents
        self.config = config or HierarchicalRetrievalConfig()

        self.embedding_model = (
            embedding_model
            if embedding_model is not None
            else SentenceTransformer(embedding_model_name)
        )
        self.cross_encoder = (
            cross_encoder
            if cross_encoder is not None
            else CrossEncoder(cross_encoder_model_name)
        )

        self.parent_retriever = HierarchicalDenseRetriever(
            documents=documents,
            model_name=embedding_model_name,
            model=self.embedding_model,
        )

    def search(self, query: str) -> HierarchicalRetrievalResult:
        cleaned_query = query.strip()
        if not cleaned_query:
            raise ValueError("query must not be blank")

        parent_ranking = self.parent_retriever.rank_documents(
            cleaned_query
        )
        selected_parent_ids = [
            document_id
            for document_id, _score
            in parent_ranking[: self.config.parent_beam]
        ]

        section_candidates = self._collect_section_candidates(
            selected_parent_ids
        )
        section_ranking = self._rank_sections(
            cleaned_query,
            section_candidates,
        )
        retained_sections = section_ranking[
            : self.config.section_beam
        ]

        windows = []
        chunk_candidates_scored = 0

        for section_candidate in retained_sections:
            window, chunk_count = self._build_local_window(
                cleaned_query,
                section_candidate,
            )
            windows.append(window)
            chunk_candidates_scored += chunk_count

        return HierarchicalRetrievalResult(
            query=cleaned_query,
            selected_parent_ids=selected_parent_ids,
            windows=windows,
            metadata={
                "parent_candidates_scored": len(self.documents),
                "section_candidates_scored": len(section_candidates),
                "retained_sections": len(retained_sections),
                "chunk_candidates_scored": chunk_candidates_scored,
            },
        )

    def _collect_section_candidates(
        self,
        selected_parent_ids: list[str],
    ) -> list[tuple[str, int, str, str, str]]:
        candidates = []

        for document_id in selected_parent_ids:
            document = self._document_by_id(document_id)

            for section_index, section in enumerate(
                document.sections
            ):
                candidates.append(
                    (
                        document_id,
                        section_index,
                        section.title,
                        render_section(document, section),
                        section.text,
                    )
                )

        return candidates

    def _rank_sections(
        self,
        query: str,
        candidates: list[tuple[str, int, str, str, str]],
    ) -> list[tuple[str, int, str, str, float]]:
        scores = self.cross_encoder.predict(
            [
                (query, retrieval_text)
                for (
                    _document_id,
                    _section_index,
                    _section_title,
                    retrieval_text,
                    _section_text,
                ) in candidates
            ]
        )

        ranked = [
            (
                document_id,
                section_index,
                section_title,
                section_text,
                float(score),
            )
            for (
                document_id,
                section_index,
                section_title,
                _retrieval_text,
                section_text,
            ), score in zip(candidates, scores)
        ]

        ranked.sort(
            key=lambda item: item[4],
            reverse=True,
        )
        return ranked

    def _build_local_window(
        self,
        query: str,
        section_candidate: tuple[str, int, str, str, float],
    ) -> tuple[HierarchicalEvidenceWindow, int]:
        (
            document_id,
            section_index,
            section_title,
            section_text,
            section_score,
        ) = section_candidate

        document = self._document_by_id(document_id)
        chunks = chunk_section(
            document,
            section_index=section_index,
            chunk_size_words=self.config.chunk_size_words,
            overlap_words=self.config.chunk_overlap_words,
        )

        chunk_scores = self.cross_encoder.predict(
            [
                (query, chunk.text)
                for chunk in chunks
            ]
        )

        scored_chunks = sorted(
            [
                (chunk, float(score))
                for chunk, score in zip(chunks, chunk_scores)
            ],
            key=lambda item: item[1],
            reverse=True,
        )

        anchor_chunk, anchor_score = scored_chunks[0]

        selected_chunks = [
            chunk
            for chunk in chunks
            if abs(
                chunk.chunk_index
                - anchor_chunk.chunk_index
            )
            <= self.config.chunk_radius
        ]

        start_word = min(
            chunk.start_word
            for chunk in selected_chunks
        )
        end_word = max(
            chunk.end_word
            for chunk in selected_chunks
        )

        words = section_text.split()
        window_text = " ".join(
            words[start_word:end_word]
        )

        return (
            HierarchicalEvidenceWindow(
                document_id=document_id,
                section_index=section_index,
                section_title=section_title,
                section_score=section_score,
                anchor_chunk_index=anchor_chunk.chunk_index,
                anchor_chunk_score=anchor_score,
                start_word=start_word,
                end_word=end_word,
                text=window_text,
            ),
            len(chunks),
        )

    def _document_by_id(
        self,
        document_id: str,
    ) -> StructuredDocument:
        document = next(
            (
                item
                for item in self.documents
                if item.document_id == document_id
            ),
            None,
        )

        if document is None:
            raise ValueError(
                f"unknown document_id={document_id}"
            )

        return document
