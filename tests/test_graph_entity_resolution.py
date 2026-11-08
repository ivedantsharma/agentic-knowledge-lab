import pytest

from knowledge_engine.graph.entity_resolution import (
    LexicalEntityResolver,
    normalize_entity_text,
)
from knowledge_engine.graph.schema import (
    ClaimGraph,
    GraphEntity,
)


def build_graph() -> ClaimGraph:
    return ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="atlas",
                name="Atlas",
                entity_type="service",
                aliases=["Atlas Service"],
            ),
            GraphEntity(
                entity_id="platform_reliability",
                name="Platform Reliability",
                entity_type="team",
                aliases=["PR Team"],
            ),
        ],
        claims=[],
    )


def test_normalize_entity_text() -> None:
    assert normalize_entity_text(
        "Platform-Reliability!"
    ) == "platform reliability"


def test_resolve_entity_by_name() -> None:
    resolver = LexicalEntityResolver(
        build_graph()
    )

    result = resolver.resolve(
        "Which team operates Atlas?"
    )

    assert result.entity_id == "atlas"
    assert result.match_type == "name"


def test_resolve_entity_by_alias() -> None:
    resolver = LexicalEntityResolver(
        build_graph()
    )

    result = resolver.resolve(
        "What does the PR Team maintain?"
    )

    assert (
        result.entity_id
        == "platform_reliability"
    )
    assert result.match_type == "alias"


def test_resolve_rejects_missing_entity() -> None:
    resolver = LexicalEntityResolver(
        build_graph()
    )

    with pytest.raises(ValueError):
        resolver.resolve(
            "What is the backup cadence?"
        )
