import pytest

from knowledge_engine.retrieval.state import RetrievalState
from scripts.run_phase3_structured_state_chain import (
    render_state_query,
)


def test_render_state_query_uses_entity_and_qualifier() -> None:
    state = RetrievalState(
        entity="Borealis",
        qualifiers=["production"],
    )

    query = render_state_query(
        "Backup cadence for {qualifier} {entity}?",
        state,
    )

    assert query == "Backup cadence for production Borealis?"


def test_render_state_query_requires_qualifier() -> None:
    with pytest.raises(ValueError):
        render_state_query(
            "Backup cadence for {qualifier} {entity}?",
            RetrievalState(entity="Borealis"),
        )
