from dataclasses import dataclass

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    KnowledgeClaim,
)
from knowledge_engine.retrieval.vector_math import cosine_similarity


@dataclass(frozen=True)
class GraphPathCandidate:
    start_entity_id: str
    relation_path: list[str]
    claim_ids: list[str]
    final_value: str
    evidence: list[EvidenceReference]
    profile: str


class GraphPathEnumerator:
    """Enumerate simple outgoing claim paths that terminate in literals."""

    def __init__(self, graph: ClaimGraph) -> None:
        self.graph = graph
        self.entities_by_id = {
            entity.entity_id: entity
            for entity in graph.entities
        }
        self.outgoing: dict[str, list[KnowledgeClaim]] = {}

        for claim in graph.claims:
            self.outgoing.setdefault(
                claim.subject_entity_id,
                [],
            ).append(claim)

    def enumerate_literal_paths(
        self,
        start_entity_id: str,
        max_hops: int = 3,
    ) -> list[GraphPathCandidate]:
        if start_entity_id not in self.entities_by_id:
            raise ValueError(
                f"unknown entity_id={start_entity_id}"
            )
        if max_hops <= 0:
            raise ValueError(
                "max_hops must be positive"
            )

        results: list[GraphPathCandidate] = []
        self._walk(
            start_entity_id=start_entity_id,
            current_entity_id=start_entity_id,
            relation_path=[],
            claim_ids=[],
            evidence=[],
            visited_entities={start_entity_id},
            max_hops=max_hops,
            results=results,
        )
        return results

    def _walk(
        self,
        start_entity_id: str,
        current_entity_id: str,
        relation_path: list[str],
        claim_ids: list[str],
        evidence: list[EvidenceReference],
        visited_entities: set[str],
        max_hops: int,
        results: list[GraphPathCandidate],
    ) -> None:
        if len(relation_path) >= max_hops:
            return

        for claim in self.outgoing.get(
            current_entity_id,
            [],
        ):
            next_relations = [
                *relation_path,
                claim.relation,
            ]
            next_claim_ids = [
                *claim_ids,
                claim.claim_id,
            ]
            next_evidence = [
                *evidence,
                *claim.evidence,
            ]

            if claim.object_value is not None:
                results.append(
                    GraphPathCandidate(
                        start_entity_id=start_entity_id,
                        relation_path=next_relations,
                        claim_ids=next_claim_ids,
                        final_value=claim.object_value,
                        evidence=next_evidence,
                        profile=self._render_profile(
                            next_relations,
                            next_evidence,
                            claim.object_value,
                        ),
                    )
                )
                continue

            next_entity_id = claim.object_entity_id
            if (
                next_entity_id is None
                or next_entity_id in visited_entities
            ):
                continue

            self._walk(
                start_entity_id=start_entity_id,
                current_entity_id=next_entity_id,
                relation_path=next_relations,
                claim_ids=next_claim_ids,
                evidence=next_evidence,
                visited_entities={
                    *visited_entities,
                    next_entity_id,
                },
                max_hops=max_hops,
                results=results,
            )

    @staticmethod
    def _render_profile(
        relation_path: list[str],
        evidence: list[EvidenceReference],
        final_value: str,
    ) -> str:
        relation_text = " -> ".join(
            relation.replace("_", " ")
            for relation in relation_path
        )
        evidence_text = " ".join(
            item.evidence_text
            for item in evidence
        )
        return (
            f"Relations: {relation_text}. "
            f"Evidence: {evidence_text} "
            f"Final value: {final_value}."
        )


@dataclass(frozen=True)
class RankedGraphPath:
    candidate: GraphPathCandidate
    score: float


class SemanticGraphPathRanker:
    def __init__(
        self,
        model_name: str,
        model: SentenceTransformer | None = None,
    ) -> None:
        self.model = (
            model
            if model is not None
            else SentenceTransformer(model_name)
        )

    def rank(
        self,
        question: str,
        candidates: list[GraphPathCandidate],
    ) -> list[RankedGraphPath]:
        if not question.strip():
            raise ValueError(
                "question must not be blank"
            )
        if not candidates:
            raise ValueError(
                "candidates must not be empty"
            )

        profiles = [
            candidate.profile
            for candidate in candidates
        ]
        profile_embeddings = self.model.encode(
            profiles
        )
        query_embedding = self.model.encode(
            question
        )

        ranked = [
            RankedGraphPath(
                candidate=candidate,
                score=cosine_similarity(
                    query_embedding,
                    embedding,
                ),
            )
            for candidate, embedding in zip(
                candidates,
                profile_embeddings,
            )
        ]
        ranked.sort(
            key=lambda item: item.score,
            reverse=True,
        )
        return ranked
