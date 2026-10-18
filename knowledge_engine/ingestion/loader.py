import json
from pathlib import Path

from pydantic import ValidationError

from knowledge_engine.ingestion.schema import SourceDocument


class SourceDocumentLoadError(ValueError):
    """Raised when source-document JSONL cannot be loaded safely."""


def load_source_documents_jsonl(path: str | Path) -> list[SourceDocument]:
    """Load source documents from JSONL."""
    source_path = Path(path)
    documents: list[SourceDocument] = []
    seen_ids: set[str] = set()

    with source_path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line:
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SourceDocumentLoadError(
                    f"Invalid JSON on line {line_number}: {exc.msg}"
                ) from exc

            try:
                document = SourceDocument.model_validate(payload)
            except ValidationError as exc:
                raise SourceDocumentLoadError(
                    f"Invalid SourceDocument on line {line_number}: {exc}"
                ) from exc

            if document.document_id in seen_ids:
                raise SourceDocumentLoadError(
                    f"Duplicate document_id '{document.document_id}' on line {line_number}"
                )

            seen_ids.add(document.document_id)
            documents.append(document)

    return documents
