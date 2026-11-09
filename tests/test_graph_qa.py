from knowledge_engine.graph.qa import (
    GraphQAPipeline,
)
from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
)


class FakeModel:
    def encode(self, values):
        if isinstance(values, str):
            if "backup" in values.lower():
                return [1.0, 0.0]
            return [0.0, 1.0]

        vectors = []
        for value in values:
            if "backup" in value.lower():
                vectors.append([1.0, 0.0])
            else:
                vectors.append([0.0, 1.0])
        return vectors


def test_graph_qa_pipeline_selects_and_traverses_path() -> None:
    graph = ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="atlas",
                name="Atlas",
                entity_type="service",
            ),
        ],
        claims=[
            KnowledgeClaim(
                claim_id="backup",
                subject_entity_id="atlas",
                relation="backup_cadence",
                object_value="daily",
                evidence=[
                    EvidenceReference(
                        document_id="backup-doc",
                        evidence_text=(
                            "Atlas backup cadence is daily."
                        ),
                    )
                ],
            ),
            KnowledgeClaim(
                claim_id="purpose",
                subject_entity_id="atlas",
                relation="purpose",
                object_value="authentication",
                evidence=[
                    EvidenceReference(
                        document_id="purpose-doc",
                        evidence_text=(
                            "Atlas provides authentication."
                        ),
                    )
                ],
            ),
        ],
    )

    pipeline = GraphQAPipeline(
        graph=graph,
        model_name="unused",
        model=FakeModel(),
        max_hops=1,
    )

    result = pipeline.answer(
        "What is the Atlas backup cadence?"
    )

    assert (
        result.entity_resolution.entity_id
        == "atlas"
    )
    assert result.claim_ids == ["backup"]
    assert result.final_value == "daily"
    assert (
        result.evidence[0].document_id
        == "backup-doc"
    )
