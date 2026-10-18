from typing import Any

from pydantic import BaseModel, Field, field_validator


class SourceDocument(BaseModel):
    """Raw logical document before chunking."""

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


class DocumentChunk(BaseModel):
    """Retrieval-ready chunk derived from one source document."""

    chunk_id: str
    source_document_id: str
    chunk_index: int
    text: str
    start_word: int
    end_word: int
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("chunk_id", "source_document_id")
    @classmethod
    def validate_required_ids(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("identifier must not be blank")

        return cleaned

    @field_validator("text")
    @classmethod
    def validate_chunk_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("chunk text must not be blank")

        return cleaned

    @field_validator("chunk_index", "start_word", "end_word")
    @classmethod
    def validate_non_negative_integer(cls, value: int) -> int:
        if value < 0:
            raise ValueError("chunk positions must be zero or greater")

        return value
