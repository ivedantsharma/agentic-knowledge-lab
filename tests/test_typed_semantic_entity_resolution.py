from knowledge_engine.graph.schema import (
    ClaimGraph,
    GraphEntity,
)
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
)


class FakeModel:
    def encode(self, values):
        if isinstance(values, str):
            return [1.0, 0.0]

        return [
            [1.0, 0.0]
            for _ in values
        ]


def test_valid_entities_for_type_filters_graph_nodes() -> None:
    graph = ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="team",
                name="Team",
                entity_type="team",
            ),
            GraphEntity(
                entity_id="service",
                name="Service",
                entity_type="service",
            ),
        ],
        claims=[],
    )

    ranker = SemanticEntityRanker(
        graph=graph,
        model_name="unused",
        model=FakeModel(),
    )

    assert ranker.valid_entities_for_type(
        "team"
    ) == {"team"}
