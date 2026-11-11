import pytest
from pydantic import ValidationError

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
    RetrievalPolicyExample,
    parse_retrieval_policy_action,
)


def test_policy_example_accepts_valid_action() -> None:
    example = RetrievalPolicyExample(
        example_id="ex-001",
        source_task_id="task-001",
        question="What is the current cadence?",
        target_action="SEARCH_HYBRID_K2",
    )

    assert (
        example.target_action
        == RetrievalPolicyAction.SEARCH_HYBRID_K2
    )


def test_policy_example_rejects_blank_question() -> None:
    with pytest.raises(ValidationError):
        RetrievalPolicyExample(
            example_id="ex-001",
            source_task_id="task-001",
            question="   ",
            target_action="REFORMULATE",
        )


def test_parser_requires_exact_action_token() -> None:
    assert (
        parse_retrieval_policy_action(
            "SEARCH_HYBRID_K5"
        )
        == RetrievalPolicyAction.SEARCH_HYBRID_K5
    )
    assert (
        parse_retrieval_policy_action(
            "I would choose SEARCH_HYBRID_K5"
        )
        is None
    )
