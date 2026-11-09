from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class KnowledgeChallenge(StrEnum):
    MULTI_HOP = "multi_hop"
    DISTRACTOR = "distractor"
    AMBIGUITY = "ambiguity"
    CONTRADICTION = "contradiction"
    STALE_KNOWLEDGE = "stale_knowledge"
    UNANSWERABLE = "unanswerable"


class KnowledgeBenchV2Task(BaseModel):
    """Hard retrieval/evidence task with explicit failure-mode labels."""

    task_id: str
    question: str
    challenge_types: set[KnowledgeChallenge] = Field(min_length=1)
    should_answer: bool
    expected_answer: str | None = None

    supporting_document_ids: set[str] = Field(default_factory=set)
    evidence_chain: list[str] = Field(default_factory=list)

    distractor_document_ids: set[str] = Field(default_factory=set)
    contradicting_document_ids: set[str] = Field(default_factory=set)
    stale_document_ids: set[str] = Field(default_factory=set)

    category: str = "knowledgebench_v2"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "task_id",
        "question",
        "category",
    )
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "required task text must not be blank"
            )
        return cleaned

    @field_validator("expected_answer")
    @classmethod
    def validate_optional_answer(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "expected_answer must not be blank"
            )
        return cleaned

    @field_validator("evidence_chain")
    @classmethod
    def validate_evidence_chain(
        cls,
        values: list[str],
    ) -> list[str]:
        cleaned = [
            value.strip()
            for value in values
        ]
        if any(not value for value in cleaned):
            raise ValueError(
                "evidence_chain IDs must not be blank"
            )
        if len(cleaned) != len(set(cleaned)):
            raise ValueError(
                "evidence_chain must not contain duplicates"
            )
        return cleaned

    @model_validator(mode="after")
    def validate_task_semantics(
        self,
    ) -> "KnowledgeBenchV2Task":
        if self.should_answer:
            if self.expected_answer is None:
                raise ValueError(
                    "answerable task requires expected_answer"
                )
            if not self.supporting_document_ids:
                raise ValueError(
                    "answerable task requires supporting documents"
                )
        else:
            if self.expected_answer is not None:
                raise ValueError(
                    "unanswerable task must not set expected_answer"
                )
            if self.supporting_document_ids:
                raise ValueError(
                    "unanswerable task must not set supporting documents"
                )
            if KnowledgeChallenge.UNANSWERABLE not in self.challenge_types:
                raise ValueError(
                    "should_answer=False requires unanswerable challenge"
                )

        if self.evidence_chain:
            if not set(self.evidence_chain).issubset(
                self.supporting_document_ids
            ):
                raise ValueError(
                    "evidence_chain must be a subset of supporting documents"
                )

        if (
            KnowledgeChallenge.MULTI_HOP in self.challenge_types
            and len(self.evidence_chain) < 2
        ):
            raise ValueError(
                "multi_hop task requires at least two evidence-chain documents"
            )

        labeled_sets = [
            self.supporting_document_ids,
            self.distractor_document_ids,
            self.contradicting_document_ids,
            self.stale_document_ids,
        ]
        labels = [
            "supporting",
            "distractor",
            "contradicting",
            "stale",
        ]

        for left_index, left in enumerate(labeled_sets):
            for right_index in range(
                left_index + 1,
                len(labeled_sets),
            ):
                overlap = left & labeled_sets[right_index]
                if overlap:
                    raise ValueError(
                        f"{labels[left_index]} and "
                        f"{labels[right_index]} document labels overlap: "
                        f"{sorted(overlap)}"
                    )

        return self
