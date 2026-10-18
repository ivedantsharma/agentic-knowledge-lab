from knowledge_engine.ingestion.markdown_parser import (
    parse_markdown_document,
)


def test_parse_markdown_document(tmp_path) -> None:
    path = tmp_path / "manual.md"

    path.write_text(
        (
            "# Example Manual\n\n"
            "## Intro\n\n"
            "Hello world.\n\n"
            "## Retry Policy\n\n"
            "Retry failed jobs three times.\n"
        ),
        encoding="utf-8",
    )

    document = parse_markdown_document(
        path,
        document_id="example",
    )

    assert document.document_id == "example"
    assert document.metadata["title"] == "Example Manual"
    assert document.metadata["source_type"] == "markdown"

    assert len(document.sections) == 2
    assert document.sections[0].title == "Intro"
    assert document.sections[0].text == "Hello world."
    assert document.sections[1].title == "Retry Policy"


def test_markdown_parser_uses_filename_when_title_missing(
    tmp_path,
) -> None:
    path = tmp_path / "fallback.md"

    path.write_text(
        "## Intro\n\nHello.",
        encoding="utf-8",
    )

    document = parse_markdown_document(path)

    assert document.document_id == "fallback"
    assert document.metadata["title"] == "fallback"
