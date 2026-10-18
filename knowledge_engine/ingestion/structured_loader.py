import json
from pathlib import Path

from knowledge_engine.ingestion.structured_schema import StructuredDocument


def load_structured_documents_json(
    path: str | Path,
) -> list[StructuredDocument]:
    """Load structured source documents from a JSON array."""
    payload = json.loads(
        Path(path).read_text(encoding="utf-8")
    )

    return [
        StructuredDocument.model_validate(item)
        for item in payload
    ]
