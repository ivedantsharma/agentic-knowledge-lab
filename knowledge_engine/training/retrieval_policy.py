from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class RetrievalPolicyAction(StrEnum):
    SEARCH_HYBRID_K1 = "SEARCH_HYBRID_K1"
    SEARCH_HYBRID_K2 = "SEARCH_HYBRID_K2"
    SEARCH_HYBRID_K3 = "SEARCH_HYBRID_K3"
    SEARCH_HYBRID_K5 = "SEARCH_HYBRID_K5"
    REFORMULATE = "REFORMULATE"


class RetrievalPolicySplit(StrEnum):
    TRAIN = "train"
    DEV = "dev"
    HELDOUT = "heldout"


class RetrievalPolicyExample(BaseModel):
    example_id: str
    source_task_id: str
    question: str
    target_action: RetrievalPolicyAction
    split: RetrievalPolicySplit | None = None
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    @field_validator(
        "example_id",
        "source_task_id",
        "question",
    )
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "retrieval policy text must not be blank"
            )
        return cleaned


def parse_retrieval_policy_action(
    output: str,
) -> RetrievalPolicyAction | None:
    cleaned = output.strip()

    try:
        return RetrievalPolicyAction(cleaned)
    except ValueError:
        return None
