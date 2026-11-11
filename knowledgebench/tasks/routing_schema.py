from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class RoutingQueryStyle(StrEnum):
    LEXICAL_EXPLICIT = "lexical_explicit"
    SEMANTIC_PARAPHRASE = "semantic_paraphrase"


class RoutingBenchmarkTask(BaseModel):
    task_id: str
    pair_id: str
    query_style: RoutingQueryStyle
    question: str
    supporting_document_ids: set[str] = Field(
        min_length=1
    )

    @field_validator(
        "task_id",
        "pair_id",
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
                "routing task text must not be blank"
            )
        return cleaned
