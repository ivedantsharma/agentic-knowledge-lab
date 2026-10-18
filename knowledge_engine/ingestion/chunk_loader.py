import json
from pathlib import Path

from pydantic import ValidationError

from knowledge_engine.ingestion.schema import DocumentChunk


class ChunkLoadError(ValueError):
    """Raised when chunk JSONL cannot be loaded safely."""


def load_chunks_jsonl(path: str | Path) -> list[DocumentChunk]:
    """Load retrieval chunks from JSONL."""
    chunk_path = Path(path)
    chunks: list[DocumentChunk] = []
    seen_ids: set[str] = set()

    with chunk_path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line:
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ChunkLoadError(
                    f"Invalid JSON on line {line_number}: {exc.msg}"
                ) from exc

            try:
                chunk = DocumentChunk.model_validate(payload)
            except ValidationError as exc:
                raise ChunkLoadError(
                    f"Invalid DocumentChunk on line {line_number}: {exc}"
                ) from exc

            if chunk.chunk_id in seen_ids:
                raise ChunkLoadError(
                    f"Duplicate chunk_id '{chunk.chunk_id}' on line {line_number}"
                )

            seen_ids.add(chunk.chunk_id)
            chunks.append(chunk)

    return chunks
