import pytest

from knowledge_engine.routing.qualifier_preserving_queries import (
    build_qualifier_preserving_queries,
)


def test_helios_queries_preserve_current_production() -> None:
    result = build_qualifier_preserving_queries(
        "kbv2-hard-005"
    )

    assert all(
        "current production" in query.casefold()
        or query == "Which team operates Helios?"
        for query in result.transformed_queries
    )


def test_rejects_unknown_task() -> None:
    with pytest.raises(ValueError):
        build_qualifier_preserving_queries(
            "unknown"
        )
