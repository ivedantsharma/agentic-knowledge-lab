from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


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


class EntityResolutionTask(BaseModel):
    task_id: str
    question: str
    expected_entity_id: str | None = None
    should_resolve: bool
    category: str = "entity_resolution"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "task_id",
        "question",
        "category",
    )
    @classmethod
    def validate_required_entity_task_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "entity-resolution task fields must not be blank"
            )
        return cleaned

    @field_validator("expected_entity_id")
    @classmethod
    def validate_optional_entity_id(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "expected_entity_id must not be blank"
            )
        return cleaned

    @model_validator(mode="after")
    def validate_resolution_expectation(
        self,
    ) -> "EntityResolutionTask":
        if self.should_resolve and self.expected_entity_id is None:
            raise ValueError(
                "resolvable task requires expected_entity_id"
            )

        if (
            not self.should_resolve
            and self.expected_entity_id is not None
        ):
            raise ValueError(
                "abstention task must not set expected_entity_id"
            )

        return self



class SemanticEntityMentionTask(BaseModel):
    task_id: str
    question: str
    mention_text: str
    expected_entity_id: str
    category: str = "semantic_entity_mention"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "task_id",
        "question",
        "mention_text",
        "expected_entity_id",
        "category",
    )
    @classmethod
    def validate_required_mention_task_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "semantic mention task fields must not be blank"
            )
        return cleaned



class RelationConstrainedEntityTask(BaseModel):
    task_id: str
    question: str
    expected_entity_id: str
    first_relation: str
    category: str = "relation_constrained_entity"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "task_id",
        "question",
        "expected_entity_id",
        "first_relation",
        "category",
    )
    @classmethod
    def validate_required_relation_task_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "relation-constrained task fields must not be blank"
            )
        return cleaned
