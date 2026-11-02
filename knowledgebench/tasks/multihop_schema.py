from typing import Any

from pydantic import BaseModel, Field, field_validator


class EvidenceHop(BaseModel):
    hop_index: int
    query: str
    query_template: str | None = None
    extraction_pattern: str | None = None
    expected_document_id: str
    expected_fact: str

    @field_validator(
        "query",
        "expected_document_id",
        "expected_fact",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("hop fields must not be blank")
        return cleaned

    @field_validator("query_template", "extraction_pattern")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("optional hop fields must not be blank")

        return cleaned


class MultiHopTask(BaseModel):
    task_id: str
    question: str
    hops: list[EvidenceHop]
    expected_answer: str
    category: str = "multi_hop"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "task_id",
        "question",
        "expected_answer",
        "category",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("task fields must not be blank")
        return cleaned
