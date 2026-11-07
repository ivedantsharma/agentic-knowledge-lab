import pytest

from knowledge_engine.agent.actions import PlannerActionType
from knowledge_engine.agent.generative_planner import (
    LocalGenerativePlanner,
)
from knowledge_engine.agent.state import PlannerState
from knowledge_engine.retrieval.state import RetrievalState


def test_parse_search_action() -> None:
    action = LocalGenerativePlanner.parse_action(
        "SEARCH: Which worker platform is maintained by "
        "Developer Productivity?"
    )

    assert action.action_type == PlannerActionType.SEARCH
    assert action.query is not None


def test_parse_stop_action() -> None:
    action = LocalGenerativePlanner.parse_action(
        "STOP: CIRRUS-DLQ"
    )

    assert action.action_type == PlannerActionType.STOP
    assert action.answer == "CIRRUS-DLQ"


def test_parse_action_rejects_invalid_protocol() -> None:
    with pytest.raises(ValueError):
        LocalGenerativePlanner.parse_action(
            "The answer is CIRRUS-DLQ"
        )


def test_prompt_preserves_original_question_and_evidence() -> None:
    state = PlannerState(
        question="Where are failed jobs sent?",
        retrieval_state=RetrievalState(
            entity="five times",
            qualifiers=[],
            source_document_id="manual_cirrus",
            evidence_text=(
                "Jobs that exhaust retries are sent to "
                "the CIRRUS-DLQ dead-letter queue."
            ),
        ),
    )

    prompt = LocalGenerativePlanner.build_prompt(state)

    assert "Where are failed jobs sent?" in prompt
    assert "CIRRUS-DLQ" in prompt
    assert "Current entity: five times" in prompt
