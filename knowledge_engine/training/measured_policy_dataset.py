from collections import defaultdict

from pydantic import BaseModel, field_validator

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
    RetrievalPolicySplit,
)


class MeasuredPolicyExample(BaseModel):
    example_id: str
    source_task_id: str
    evidence_family: str
    split: RetrievalPolicySplit
    question: str
    target_action: RetrievalPolicyAction
    label_source: str

    @field_validator(
        "example_id",
        "source_task_id",
        "evidence_family",
        "question",
        "label_source",
    )
    @classmethod
    def clean_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "measured policy text must not be blank"
            )
        return cleaned


def evidence_family_leakage(
    examples: list[MeasuredPolicyExample],
) -> dict[str, tuple[str, ...]]:
    splits_by_family: dict[
        str,
        set[str],
    ] = defaultdict(set)

    for example in examples:
        splits_by_family[
            example.evidence_family
        ].add(
            example.split.value
        )

    return {
        family: tuple(sorted(splits))
        for family, splits
        in splits_by_family.items()
        if len(splits) > 1
    }
