import pytest
from pydantic import ValidationError

from knowledgebench.tasks.routing_schema import (
    RoutingBenchmarkTask,
    RoutingQueryStyle,
)


def test_routing_task_accepts_valid_pair() -> None:
    task = RoutingBenchmarkTask(
        task_id="rt-001",
        pair_id="borealis",
        query_style=(
            RoutingQueryStyle.LEXICAL_EXPLICIT
        ),
        question="What is the Borealis cadence?",
        supporting_document_ids={"doc-1"},
    )

    assert task.pair_id == "borealis"


def test_routing_task_rejects_blank_question() -> None:
    with pytest.raises(ValidationError):
        RoutingBenchmarkTask(
            task_id="rt-001",
            pair_id="borealis",
            query_style="lexical_explicit",
            question="   ",
            supporting_document_ids={"doc-1"},
        )
