from dataclasses import dataclass

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.retrieval.vector_math import cosine_similarity


@dataclass(frozen=True)
class SemanticEntityCandidate:
    entity_id: str
    score: float
    retrieval_text: str


def render_entity_profile(
    graph: ClaimGraph,
    entity_id: str,
) -> str:
    entity = next(
        item
        for item in graph.entities
        if item.entity_id == entity_id
    )

    parts = [
        f"Entity: {entity.name}.",
        f"Type: {entity.entity_type}.",
    ]

    if entity.aliases:
        parts.append(
            "Aliases: "
            + ", ".join(entity.aliases)
            + "."
        )

    for claim in graph.claims:
        if (
            claim.subject_entity_id == entity_id
            or claim.object_entity_id == entity_id
        ):
            parts.extend(
                evidence.evidence_text
                for evidence in claim.evidence
            )

    return " ".join(parts)


class SemanticEntityRanker:
    """Rank graph entities using semantic similarity over entity profiles."""

    def __init__(
        self,
        graph: ClaimGraph,
        model_name: str,
        model: SentenceTransformer | None = None,
    ) -> None:
        self.graph = graph
        self.model = (
            model
            if model is not None
            else SentenceTransformer(model_name)
        )

        self.entity_profiles = {
            entity.entity_id: render_entity_profile(
                graph,
                entity.entity_id,
            )
            for entity in graph.entities
        }

        self.entity_embeddings = {
            entity_id: embedding
            for entity_id, embedding in zip(
                self.entity_profiles,
                self.model.encode(
                    list(
                        self.entity_profiles.values()
                    )
                ),
            )
        }

    def rank(
        self,
        question: str,
        allowed_entity_ids: set[str] | None = None,
    ) -> list[SemanticEntityCandidate]:
        cleaned = question.strip()
        if not cleaned:
            raise ValueError(
                "question must not be blank"
            )

        query_embedding = self.model.encode(
            cleaned
        )

        candidates = [
            SemanticEntityCandidate(
                entity_id=entity_id,
                score=cosine_similarity(
                    query_embedding,
                    entity_embedding,
                ),
                retrieval_text=(
                    self.entity_profiles[entity_id]
                ),
            )
            for entity_id, entity_embedding
            in self.entity_embeddings.items()
            if (
                allowed_entity_ids is None
                or entity_id in allowed_entity_ids
            )
        ]

        if not candidates:
            raise ValueError(
                "no semantic entity candidates available"
            )

        candidates.sort(
            key=lambda item: item.score,
            reverse=True,
        )
        return candidates

    def valid_subjects_for_relation(
        self,
        relation: str,
    ) -> set[str]:
        cleaned = relation.strip()
        if not cleaned:
            raise ValueError(
                "relation must not be blank"
            )

        return {
            claim.subject_entity_id
            for claim in self.graph.claims
            if claim.relation == cleaned
        }

    def rank_for_relation(
        self,
        question: str,
        relation: str,
    ) -> list[SemanticEntityCandidate]:
        allowed = self.valid_subjects_for_relation(
            relation
        )

        if not allowed:
            raise ValueError(
                f"unknown relation={relation}"
            )

        return self.rank(
            question,
            allowed_entity_ids=allowed,
        )



@dataclass(frozen=True)
class ThresholdedEntityResolutionResult:
    entity_id: str | None
    score: float
    accepted: bool


class ThresholdedSemanticEntityResolver:
    """Accept semantic top-1 only when it clears a configured threshold."""

    def __init__(
        self,
        ranker: SemanticEntityRanker,
        threshold: float,
    ) -> None:
        self.ranker = ranker
        self.threshold = threshold

    def resolve(
        self,
        mention_text: str,
    ) -> ThresholdedEntityResolutionResult:
        ranking = self.ranker.rank(
            mention_text
        )
        top = ranking[0]

        accepted = (
            top.score >= self.threshold
        )

        return ThresholdedEntityResolutionResult(
            entity_id=(
                top.entity_id
                if accepted
                else None
            ),
            score=float(top.score),
            accepted=accepted,
        )
