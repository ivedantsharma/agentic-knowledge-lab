import json
from pathlib import Path

from knowledge_engine.graph.entity_resolution import (
    LexicalEntityResolver,
)
from knowledge_engine.graph.schema import ClaimGraph
from knowledgebench.tasks.graph_schema import EntityResolutionTask


GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_entity_resolution_stress_tasks_v0.json"
)


def load_graph_and_tasks():
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        EntityResolutionTask.model_validate(item)
        for item in json.loads(
            TASK_PATH.read_text(encoding="utf-8")
        )
    ]
    return graph, tasks


def test_longest_match_prefers_atlas_analytics() -> None:
    graph, _tasks = load_graph_and_tasks()
    resolver = LexicalEntityResolver(graph)

    result = resolver.resolve(
        "Which group owns Atlas Analytics reporting?"
    )

    assert result.entity_id == "atlas_analytics"


def test_alias_resolution_works() -> None:
    graph, _tasks = load_graph_and_tasks()
    resolver = LexicalEntityResolver(graph)

    result = resolver.resolve(
        "What storage system does the PR Team maintain?"
    )

    assert result.entity_id == "platform_reliability"
    assert result.match_type == "alias"


def test_implicit_entity_abstains() -> None:
    graph, _tasks = load_graph_and_tasks()
    resolver = LexicalEntityResolver(graph)

    try:
        resolver.resolve(
            "What is the backup cadence of the customer-profile storage platform?"
        )
    except ValueError as exc:
        assert "no graph entity" in str(exc)
    else:
        raise AssertionError(
            "implicit entity should not resolve lexically"
        )
