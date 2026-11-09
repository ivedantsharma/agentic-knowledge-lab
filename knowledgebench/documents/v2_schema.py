from typing import Any

from pydantic import BaseModel, Field, field_validator


class KnowledgeBenchV2Document(BaseModel):
    """Benchmark document with optional temporal/source annotations."""

    document_id: str
    title: str
    text: str
    source_type: str
    effective_at: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "document_id",
        "title",
        "text",
        "source_type",
    )
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "required document text must not be blank"
            )
        return cleaned

    @field_validator("effective_at")
    @classmethod
    def validate_optional_effective_at(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "effective_at must not be blank"
            )
        return cleaned
