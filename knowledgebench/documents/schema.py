from typing import Any

from pydantic import BaseModel, Field, field_validator


class KnowledgeDocument(BaseModel):
    """One document in the KnowledgeBench corpus."""

    document_id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("document_id")
    @classmethod
    def validate_document_id(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("document_id must not be blank")

        return cleaned

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("text must not be blank")

        return cleaned
