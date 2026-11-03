import pytest

from knowledge_engine.agent.query_renderer import (
    render_state_query,
)
from knowledge_engine.retrieval.state import RetrievalState


def test_render_state_query_uses_structured_state() -> None:
    state = RetrievalState(
        entity="Borealis",
        qualifiers=["production"],
    )

    query = render_state_query(
        "Backup cadence for {qualifier} {entity}?",
        state,
    )

    assert query == "Backup cadence for production Borealis?"


def test_render_state_query_requires_entity() -> None:
    with pytest.raises(ValueError):
        render_state_query(
            "Who owns {entity}?",
            RetrievalState(),
        )
