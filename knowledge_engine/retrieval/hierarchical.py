from dataclasses import dataclass

from sentence_transformers import SentenceTransformer

from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)
from knowledge_engine.retrieval.vector_math import cosine_similarity


@dataclass(frozen=True)
class HierarchicalSearchResult:
    document_id: str
    section_index: int
    section_title: str
    section_text: str
    document_score: float
    section_score: float


def render_document_summary(
    document: StructuredDocument,
) -> str:
    title = str(
        document.metadata.get(
            "title",
            document.document_id,
        )
    )
    section_titles = ", ".join(
        section.title
        for section in document.sections
    )

    return (
        f"Document: {title}. "
        f"Sections: {section_titles}."
    )


def render_section(
    document: StructuredDocument,
    section: DocumentSection,
) -> str:
    title = str(
        document.metadata.get(
            "title",
            document.document_id,
        )
    )

    return (
        f"Document: {title}. "
        f"Section: {section.title}. "
        f"{section.text}"
    )


class HierarchicalDenseRetriever:
    """Dense document-first, section-second retrieval."""

    def __init__(
        self,
        documents: list[StructuredDocument],
        model_name: str,
        model: SentenceTransformer | None = None,
    ) -> None:
        if not documents:
            raise ValueError(
                "hierarchical retriever requires documents"
            )

        self.documents = documents
        self.model = (
            model
            if model is not None
            else SentenceTransformer(model_name)
        )

        self.document_embeddings = self.model.encode(
            [
                render_document_summary(document)
                for document in documents
            ]
        )

        self.section_embeddings: dict[str, list] = {
            document.document_id: self.model.encode(
                [
                    render_section(document, section)
                    for section in document.sections
                ]
            )
            for document in documents
        }

    def rank_documents(
        self,
        query: str,
    ) -> list[tuple[str, float]]:
        query_embedding = list(
            map(float, self.model.encode(query))
        )

        ranked = [
            (
                document.document_id,
                cosine_similarity(
                    query_embedding,
                    list(map(float, embedding)),
                ),
            )
            for document, embedding in zip(
                self.documents,
                self.document_embeddings,
            )
        ]

        ranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return ranked

    def rank_sections(
        self,
        query: str,
        document_id: str,
    ) -> list[tuple[int, str, float]]:
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

        query_embedding = list(
            map(float, self.model.encode(query))
        )

        embeddings = self.section_embeddings[
            document_id
        ]

        ranked = [
            (
                index,
                section.title,
                cosine_similarity(
                    query_embedding,
                    list(map(float, embedding)),
                ),
            )
            for index, (section, embedding) in enumerate(
                zip(document.sections, embeddings)
            )
        ]

        ranked.sort(
            key=lambda item: item[2],
            reverse=True,
        )

        return ranked

    def search(
        self,
        query: str,
    ) -> HierarchicalSearchResult:
        document_ranking = self.rank_documents(
            query
        )
        document_id, document_score = (
            document_ranking[0]
        )

        section_ranking = self.rank_sections(
            query,
            document_id,
        )
        section_index, section_title, section_score = (
            section_ranking[0]
        )

        document = next(
            item
            for item in self.documents
            if item.document_id == document_id
        )

        return HierarchicalSearchResult(
            document_id=document_id,
            section_index=section_index,
            section_title=section_title,
            section_text=document.sections[
                section_index
            ].text,
            document_score=document_score,
            section_score=section_score,
        )