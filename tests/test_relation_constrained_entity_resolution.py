from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
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


def build_graph() -> ClaimGraph:
    return ClaimGraph(
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
        claims=[
            KnowledgeClaim(
                claim_id="claim-1",
                subject_entity_id="team",
                relation="maintains",
                object_entity_id="service",
                evidence=[
                    EvidenceReference(
                        document_id="doc",
                        evidence_text="Team maintains Service.",
                    )
                ],
            )
        ],
    )


def test_valid_subjects_for_relation() -> None:
    ranker = SemanticEntityRanker(
        graph=build_graph(),
        model_name="unused",
        model=FakeModel(),
    )

    assert ranker.valid_subjects_for_relation(
        "maintains"
    ) == {"team"}


def test_rank_for_relation_filters_invalid_subjects() -> None:
    ranker = SemanticEntityRanker(
        graph=build_graph(),
        model_name="unused",
        model=FakeModel(),
    )

    ranking = ranker.rank_for_relation(
        "Who maintains the service?",
        "maintains",
    )

    assert [
        item.entity_id
        for item in ranking
    ] == ["team"]
