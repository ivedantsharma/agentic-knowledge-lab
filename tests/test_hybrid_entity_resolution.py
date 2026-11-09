from knowledge_engine.graph.hybrid_entity_resolution import (
    HybridEntityResolver,
)
from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
)


class FakeModel:
    def encode(self, values):
        mapping = {
            "Entity: Borealis. Type: service. Borealis stores production customer profiles.":
                [1.0, 0.0],
            "Entity: Cirrus. Type: service. Cirrus runs asynchronous jobs.":
                [0.0, 1.0],
        }

        if isinstance(values, str):
            if "customer profile" in values:
                return [1.0, 0.0]
            return [0.0, 1.0]

        return [
            mapping[value]
            for value in values
        ]


def build_graph() -> ClaimGraph:
    return ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="borealis",
                name="Borealis",
                entity_type="service",
            ),
            GraphEntity(
                entity_id="cirrus",
                name="Cirrus",
                entity_type="service",
            ),
        ],
        claims=[
            KnowledgeClaim(
                claim_id="b",
                subject_entity_id="borealis",
                relation="stores",
                object_value="profiles",
                evidence=[
                    EvidenceReference(
                        document_id="db",
                        evidence_text=(
                            "Borealis stores production customer profiles."
                        ),
                    )
                ],
            ),
            KnowledgeClaim(
                claim_id="c",
                subject_entity_id="cirrus",
                relation="runs",
                object_value="jobs",
                evidence=[
                    EvidenceReference(
                        document_id="dc",
                        evidence_text=(
                            "Cirrus runs asynchronous jobs."
                        ),
                    )
                ],
            ),
        ],
    )


def test_hybrid_resolver_prefers_lexical_match() -> None:
    resolver = HybridEntityResolver(
        graph=build_graph(),
        model_name="unused",
        threshold=0.39,
        model=FakeModel(),
    )

    result = resolver.resolve(
        "What does Borealis store?"
    )

    assert result.entity_id == "borealis"
    assert result.match_type == "name"


def test_hybrid_resolver_uses_typed_semantic_fallback() -> None:
    resolver = HybridEntityResolver(
        graph=build_graph(),
        model_name="unused",
        threshold=0.39,
        model=FakeModel(),
    )

    result = resolver.resolve(
        "Which service stores production customer profiles?"
    )

    assert result.entity_id == "borealis"
    assert result.match_type == "semantic_service"
