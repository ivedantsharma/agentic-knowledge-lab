from typing import Any

from pydantic import BaseModel, Field, field_validator


class RunResult(BaseModel):
    """Observed output from running a system on one KnowledgeBench task."""

    task_id: str
    generated_answer: str | None = None
    retrieved_document_ids: list[str] = Field(default_factory=list)
    tool_calls: int = 0
    latency_ms: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("task_id must not be blank")

        return cleaned

    @field_validator("tool_calls")
    @classmethod
    def validate_tool_calls(cls, value: int) -> int:
        if value < 0:
            raise ValueError("tool_calls must be zero or greater")

        return value

    @field_validator("latency_ms")
    @classmethod
    def validate_latency_ms(cls, value: float | None) -> float | None:
        if value is not None and value < 0:
            raise ValueError("latency_ms must be zero or greater")

        return value
