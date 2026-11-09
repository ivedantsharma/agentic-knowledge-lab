from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class AgentActionType(StrEnum):
    SEARCH = "search"
    STOP = "stop"


class AgentTraceStep(BaseModel):
    step_index: int = Field(ge=0)
    action_type: AgentActionType
    query: str | None = None
    retrieved_document_ids: list[str] = Field(
        default_factory=list
    )
    answer: str | None = None
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    @field_validator("query", "answer")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "optional trace text must not be blank"
            )
        return cleaned

    @model_validator(mode="after")
    def validate_action_shape(
        self,
    ) -> "AgentTraceStep":
        if self.action_type == AgentActionType.SEARCH:
            if self.query is None:
                raise ValueError(
                    "SEARCH step requires query"
                )
            if self.answer is not None:
                raise ValueError(
                    "SEARCH step must not contain answer"
                )
        else:
            if self.answer is None:
                raise ValueError(
                    "STOP step requires answer"
                )
            if self.query is not None:
                raise ValueError(
                    "STOP step must not contain query"
                )
            if self.retrieved_document_ids:
                raise ValueError(
                    "STOP step must not retrieve documents"
                )
        return self


class AgentRunTrace(BaseModel):
    task_id: str
    steps: list[AgentTraceStep] = Field(
        min_length=1
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    @field_validator("task_id")
    @classmethod
    def validate_task_id(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "task_id must not be blank"
            )
        return cleaned

    @model_validator(mode="after")
    def validate_step_order(
        self,
    ) -> "AgentRunTrace":
        expected = list(
            range(len(self.steps))
        )
        observed = [
            step.step_index
            for step in self.steps
        ]
        if observed != expected:
            raise ValueError(
                "trace step_index values must be contiguous "
                "and start at zero"
            )

        stop_indices = [
            index
            for index, step in enumerate(self.steps)
            if step.action_type == AgentActionType.STOP
        ]
        if len(stop_indices) > 1:
            raise ValueError(
                "trace may contain at most one STOP"
            )
        if (
            stop_indices
            and stop_indices[0] != len(self.steps) - 1
        ):
            raise ValueError(
                "STOP must be the final trace step"
            )
        return self
