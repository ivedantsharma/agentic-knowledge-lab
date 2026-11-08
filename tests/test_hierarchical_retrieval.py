from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)
from knowledge_engine.retrieval.hierarchical import (
    render_document_summary,
    render_section,
)


def test_render_document_summary_includes_parent_and_children() -> None:
    document = StructuredDocument(
        document_id="manual",
        metadata={"title": "Service Manual"},
        sections=[
            DocumentSection(
                title="Overview",
                text="Overview text.",
            ),
            DocumentSection(
                title="Backup Policy",
                text="Backups run daily.",
            ),
        ],
    )

    rendered = render_document_summary(
        document
    )

    assert "Service Manual" in rendered
    assert "Overview" in rendered
    assert "Backup Policy" in rendered


def test_render_section_preserves_parent_context() -> None:
    document = StructuredDocument(
        document_id="manual",
        metadata={"title": "Service Manual"},
        sections=[
            DocumentSection(
                title="Backup Policy",
                text="Backups run daily.",
            )
        ],
    )

    rendered = render_section(
        document,
        document.sections[0],
    )

    assert "Service Manual" in rendered
    assert "Backup Policy" in rendered
    assert "Backups run daily." in rendered