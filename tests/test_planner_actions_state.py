import pytest
from pydantic import ValidationError

from knowledge_engine.agent.actions import (
    PlannerAction,
    PlannerActionType,
)
from knowledge_engine.agent.state import PlannerState


def test_search_action_requires_query() -> None:
    with pytest.raises(ValidationError):
        PlannerAction(
            action_type=PlannerActionType.SEARCH,
        )


def test_stop_action_requires_answer() -> None:
    with pytest.raises(ValidationError):
        PlannerAction(
            action_type=PlannerActionType.STOP,
        )


def test_planner_state_starts_empty() -> None:
    state = PlannerState(
        question="What is the answer?"
    )

    assert state.step_index == 0
    assert state.trace == []
    assert state.stopped is False
    assert state.final_answer is None
