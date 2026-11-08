from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
)
from knowledge_engine.graph.semantic_entity_resolution import (
    render_entity_profile,
)


def test_entity_profile_includes_neighbor_evidence() -> None:
    graph = ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="team",
                name="Platform Reliability",
                entity_type="team",
            ),
            GraphEntity(
                entity_id="service",
                name="Borealis",
                entity_type="service",
            ),
        ],
        claims=[
            KnowledgeClaim(
                claim_id="claim-1",
                subject_entity_id="team",
                relation="maintains",
                object_entity_id="service",
                evidence=[
                    EvidenceReference(
                        document_id="doc",
                        evidence_text=(
                            "Platform Reliability maintains "
                            "the Borealis storage system."
                        ),
                    )
                ],
            )
        ],
    )

    profile = render_entity_profile(
        graph,
        "service",
    )

    assert "Borealis" in profile
    assert "storage system" in profile


def test_entity_profile_includes_aliases() -> None:
    graph = ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="team",
                name="Platform Reliability",
                entity_type="team",
                aliases=["PR Team"],
            )
        ],
        claims=[],
    )

    profile = render_entity_profile(
        graph,
        "team",
    )

    assert "PR Team" in profile
