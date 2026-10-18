from pathlib import Path

from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)


def parse_markdown_document(
    path: str | Path,
    document_id: str | None = None,
) -> StructuredDocument:
    """Parse a simple heading-based Markdown document."""
    markdown_path = Path(path)
    lines = markdown_path.read_text(
        encoding="utf-8"
    ).splitlines()

    title: str | None = None
    current_section_title: str | None = None
    current_body: list[str] = []
    sections: list[DocumentSection] = []

    def flush_section() -> None:
        nonlocal current_section_title, current_body

        if current_section_title is None:
            return

        text = " ".join(
            line.strip()
            for line in current_body
            if line.strip()
        ).strip()

        if text:
            sections.append(
                DocumentSection(
                    title=current_section_title,
                    text=text,
                )
            )

        current_body = []

    for raw_line in lines:
        line = raw_line.strip()

        if line.startswith("# "):
            if title is None:
                title = line[2:].strip()
            continue

        if line.startswith("## ") or line.startswith("### "):
            flush_section()

            heading_prefix = "### " if line.startswith("### ") else "## "
            current_section_title = line[len(heading_prefix):].strip()
            current_body = []
            continue

        if current_section_title is not None:
            current_body.append(raw_line)

    flush_section()

    if title is None:
        title = markdown_path.stem

    resolved_document_id = (
        document_id
        if document_id is not None
        else markdown_path.stem
    )

    return StructuredDocument(
        document_id=resolved_document_id,
        sections=sections,
        metadata={
            "source_type": "markdown",
            "source_path": str(markdown_path),
            "title": title,
        },
    )
