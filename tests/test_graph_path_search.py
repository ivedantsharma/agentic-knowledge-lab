from knowledge_engine.graph.path_search import (
    GraphPathEnumerator,
)
from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
)


def test_enumerator_finds_branching_literal_paths() -> None:
    graph = ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="a",
                name="A",
                entity_type="service",
            ),
            GraphEntity(
                entity_id="b",
                name="B",
                entity_type="team",
            ),
        ],
        claims=[
            KnowledgeClaim(
                claim_id="c1",
                subject_entity_id="a",
                relation="owned_by",
                object_entity_id="b",
                evidence=[
                    EvidenceReference(
                        document_id="d1",
                        evidence_text="A is owned by B.",
                    )
                ],
            ),
            KnowledgeClaim(
                claim_id="c2",
                subject_entity_id="b",
                relation="cadence",
                object_value="daily",
                evidence=[
                    EvidenceReference(
                        document_id="d2",
                        evidence_text="B runs daily.",
                    )
                ],
            ),
            KnowledgeClaim(
                claim_id="c3",
                subject_entity_id="a",
                relation="snapshot",
                object_value="weekly",
                evidence=[
                    EvidenceReference(
                        document_id="d3",
                        evidence_text="A snapshots weekly.",
                    )
                ],
            ),
        ],
    )

    paths = GraphPathEnumerator(
        graph
    ).enumerate_literal_paths(
        "a",
        max_hops=2,
    )

    assert {
        tuple(path.relation_path)
        for path in paths
    } == {
        ("owned_by", "cadence"),
        ("snapshot",),
    }
