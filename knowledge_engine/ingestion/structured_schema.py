from typing import Any

from pydantic import BaseModel, Field, field_validator


class DocumentSection(BaseModel):
    title: str
    text: str
    context: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title", "text")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("section title/text must not be blank")
        return cleaned

    @field_validator("context")
    @classmethod
    def validate_optional_context(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("section context must not be blank")

        return cleaned


class StructuredDocument(BaseModel):
    document_id: str
    sections: list[DocumentSection]
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("document_id")
    @classmethod
    def validate_document_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("document_id must not be blank")
        return cleaned
