import pytest
from pydantic import ValidationError

from knowledgebench.tasks.query_transformation_schema import (
    OracleQueryTransformation,
)


def test_accepts_valid_oracle_transformation() -> None:
    transformation = OracleQueryTransformation(
        task_id="t1",
        original_question="What does the service do?",
        supporting_document_ids={"d1", "d2"},
        transformed_queries=[
            "Which service is maintained by Team A?",
            "What does Service B do?",
        ],
    )

    assert len(transformation.transformed_queries) == 2


def test_rejects_blank_transformed_query() -> None:
    with pytest.raises(ValidationError):
        OracleQueryTransformation(
            task_id="t1",
            original_question="Question",
            supporting_document_ids={"d1"},
            transformed_queries=["   "],
        )
