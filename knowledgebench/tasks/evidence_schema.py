from typing import Any

from pydantic import BaseModel, Field, field_validator


class EvidenceTask(BaseModel):
    """Source-level retrieval task independent of a chunking configuration."""

    task_id: str
    question: str
    source_document_id: str
    evidence_text: str
    expected_answer: str | None = None
    category: str = "chunk_retrieval"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "task_id",
        "question",
        "source_document_id",
        "evidence_text",
        "category",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("required text fields must not be blank")

        return cleaned
