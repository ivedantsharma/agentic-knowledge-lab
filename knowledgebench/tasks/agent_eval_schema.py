from typing import Any

from pydantic import BaseModel, Field, field_validator


class AgentEvalTask(BaseModel):
    """Ground truth for deterministic agent-trace evaluation."""

    task_id: str
    question: str
    expected_answer: str
    required_document_ids: list[str] = Field(
        min_length=1
    )
    max_reasonable_search_steps: int = Field(
        ge=1
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    @field_validator(
        "task_id",
        "question",
        "expected_answer",
    )
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "agent-eval task text must not be blank"
            )
        return cleaned

    @field_validator("required_document_ids")
    @classmethod
    def validate_required_documents(
        cls,
        values: list[str],
    ) -> list[str]:
        cleaned = [
            value.strip()
            for value in values
        ]
        if any(not value for value in cleaned):
            raise ValueError(
                "required document IDs must not be blank"
            )
        if len(cleaned) != len(set(cleaned)):
            raise ValueError(
                "required document IDs must be unique"
            )
        return cleaned
