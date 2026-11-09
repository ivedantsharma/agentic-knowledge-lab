from dataclasses import replace

from knowledge_engine.graph.path_search import (
    GraphPathCandidate,
    RankedGraphPath,
)
from knowledge_engine.graph.qa import (
    ClaimGraphQAEngine,
)
from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
)


class FakePathRanker:
    def rank(self, question, candidates):
        del question
        ranked = [
            RankedGraphPath(
                candidate=candidate,
                score=(
                    0.9
                    if candidate.final_value == "daily"
                    else 0.4
                ),
            )
            for candidate in candidates
        ]
        return sorted(
            ranked,
            key=lambda item: item.score,
            reverse=True,
        )


def build_graph() -> ClaimGraph:
    return ClaimGraph(
        entities=[
            GraphEntity(
                entity_id="atlas",
                name="Atlas",
                entity_type="service",
            ),
            GraphEntity(
                entity_id="team",
                name="Team",
                entity_type="team",
            ),
        ],
        claims=[
            KnowledgeClaim(
                claim_id="c1",
                subject_entity_id="atlas",
                relation="owned_by",
                object_entity_id="team",
                evidence=[
                    EvidenceReference(
                        document_id="d1",
                        evidence_text="Atlas is owned by Team.",
                    )
                ],
            ),
            KnowledgeClaim(
                claim_id="c2",
                subject_entity_id="team",
                relation="cadence",
                object_value="daily",
                evidence=[
                    EvidenceReference(
                        document_id="d2",
                        evidence_text="Team runs daily.",
                    )
                ],
            ),
            KnowledgeClaim(
                claim_id="c3",
                subject_entity_id="atlas",
                relation="snapshot",
                object_value="weekly",
                evidence=[
                    EvidenceReference(
                        document_id="d3",
                        evidence_text="Atlas snapshots weekly.",
                    )
                ],
            ),
        ],
    )


def test_graph_qa_engine_links_ranks_and_preserves_evidence() -> None:
    engine = ClaimGraphQAEngine(
        graph=build_graph(),
        path_ranker=FakePathRanker(),
        max_hops=2,
    )

    result = engine.answer(
        "What cadence is used by the team that owns Atlas?"
    )

    assert result.entity_resolution.entity_id == "atlas"
    assert result.relation_path == [
        "owned_by",
        "cadence",
    ]
    assert result.claim_ids == ["c1", "c2"]
    assert result.answer == "daily"
    assert [
        item.document_id
        for item in result.evidence
    ] == ["d1", "d2"]
    assert result.path_score_margin == 0.5


def test_graph_qa_engine_rejects_question_without_entity() -> None:
    engine = ClaimGraphQAEngine(
        graph=build_graph(),
        path_ranker=FakePathRanker(),
        max_hops=2,
    )

    try:
        engine.answer(
            "What cadence is used?"
        )
    except ValueError as exc:
        assert "no graph entity" in str(exc)
    else:
        raise AssertionError(
            "question without explicit entity should fail"
        )
