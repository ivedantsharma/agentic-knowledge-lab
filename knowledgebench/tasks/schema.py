from typing import Any

from pydantic import BaseModel, Field, field_validator


class KnowledgeTask(BaseModel):
    """Ground-truth definition of one KnowledgeBench task."""

    task_id: str
    question: str
    relevant_document_ids: set[str] = Field(default_factory=set)
    category: str
    expected_answer: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, value: str) -> str:
        # TODO: reject empty/whitespace-only task IDs.
        raise NotImplementedError

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        # TODO: reject empty/whitespace-only questions.
        raise NotImplementedError

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        # TODO: reject empty/whitespace-only categories.
        raise NotImplementedError
