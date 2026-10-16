import json
from pathlib import Path

from pydantic import ValidationError

from knowledgebench.documents.schema import KnowledgeDocument


class DocumentLoadError(ValueError):
    """Raised when a document corpus cannot be loaded safely."""


def load_documents_jsonl(path: str | Path) -> list[KnowledgeDocument]:
    """Load and validate KnowledgeBench documents from a JSONL file."""
    corpus_path = Path(path)
    documents: list[KnowledgeDocument] = []
    seen_document_ids: set[str] = set()

    with corpus_path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line:
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise DocumentLoadError(
                    f"Invalid JSON on line {line_number}: {exc.msg}"
                ) from exc

            try:
                document = KnowledgeDocument.model_validate(payload)
            except ValidationError as exc:
                raise DocumentLoadError(
                    f"Invalid KnowledgeDocument on line {line_number}: {exc}"
                ) from exc

            if document.document_id in seen_document_ids:
                raise DocumentLoadError(
                    f"Duplicate document_id '{document.document_id}' on line {line_number}"
                )

            seen_document_ids.add(document.document_id)
            documents.append(document)

    return documents
