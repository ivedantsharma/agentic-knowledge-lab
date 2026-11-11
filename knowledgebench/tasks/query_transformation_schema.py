from pydantic import BaseModel, Field, field_validator


class OracleQueryTransformation(BaseModel):
    task_id: str
    original_question: str
    supporting_document_ids: set[str] = Field(
        min_length=1
    )
    transformed_queries: list[str] = Field(
        min_length=1
    )

    @field_validator(
        "task_id",
        "original_question",
    )
    @classmethod
    def validate_required_text(
        cls,
        value: str,
    ) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "transformation text must not be blank"
            )
        return cleaned

    @field_validator("transformed_queries")
    @classmethod
    def validate_queries(
        cls,
        values: list[str],
    ) -> list[str]:
        cleaned = [
            value.strip()
            for value in values
        ]
        if any(not value for value in cleaned):
            raise ValueError(
                "transformed queries must not be blank"
            )
        return cleaned
