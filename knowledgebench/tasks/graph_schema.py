from typing import Any

from pydantic import BaseModel, Field, field_validator


class GraphTraversalTask(BaseModel):
    task_id: str
    question: str
    start_entity_id: str
    relation_path: list[str] = Field(min_length=1)
    expected_answer: str
    expected_claim_ids: list[str] = Field(min_length=1)
    category: str = "graph_traversal"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "task_id",
        "question",
        "start_entity_id",
        "expected_answer",
        "category",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("task fields must not be blank")
        return cleaned

    @field_validator("relation_path", "expected_claim_ids")
    @classmethod
    def validate_string_lists(
        cls,
        values: list[str],
    ) -> list[str]:
        cleaned = [
            value.strip()
            for value in values
        ]

        if any(
            not value
            for value in cleaned
        ):
            raise ValueError(
                "task relation/claim IDs must not be blank"
            )

        return cleaned
