import pytest

from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
)
from knowledge_engine.graph.traversal import ClaimGraphIndex


def build_graph() -> ClaimGraph:
    return ClaimGraph(
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
                        document_id="doc1",
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
                        document_id="doc2",
                        evidence_text="B runs daily.",
                    )
                ],
            ),
        ],
    )


def test_claim_requires_exactly_one_object() -> None:
    with pytest.raises(ValueError):
        KnowledgeClaim(
            claim_id="bad",
            subject_entity_id="a",
            relation="r",
            evidence=[
                EvidenceReference(
                    document_id="doc",
                    evidence_text="evidence",
                )
            ],
        )


def test_traverse_entity_then_literal_with_evidence() -> None:
    index = ClaimGraphIndex(
        build_graph()
    )

    result = index.traverse(
        start_entity_id="a",
        relation_path=[
            "owned_by",
            "cadence",
        ],
    )

    assert result.final_value == "daily"
    assert result.claim_ids == ["c1", "c2"]
    assert [
        item.document_id
        for item in result.evidence
    ] == ["doc1", "doc2"]


def test_literal_cannot_be_intermediate_hop() -> None:
    index = ClaimGraphIndex(
        build_graph()
    )

    with pytest.raises(ValueError):
        index.traverse(
            start_entity_id="b",
            relation_path=[
                "cadence",
                "something_else",
            ],
        )
