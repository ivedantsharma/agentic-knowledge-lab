from dataclasses import dataclass

from knowledge_engine.graph.entity_resolution import (
    EntityResolutionResult,
    LexicalEntityResolver,
)
from knowledge_engine.graph.path_search import (
    GraphPathEnumerator,
    RankedGraphPath,
    SemanticGraphPathRanker,
)
from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
)


@dataclass(frozen=True)
class GraphQAResult:
    question: str
    entity_resolution: EntityResolutionResult
    relation_path: list[str]
    claim_ids: list[str]
    answer: str
    evidence: list[EvidenceReference]
    top_path_score: float
    second_path_score: float | None
    path_score_margin: float | None
    candidate_path_count: int


class ClaimGraphQAEngine:
    """End-to-end explicit-entity claim-graph QA baseline."""

    def __init__(
        self,
        graph: ClaimGraph,
        path_ranker: SemanticGraphPathRanker,
        max_hops: int = 3,
    ) -> None:
        if max_hops <= 0:
            raise ValueError(
                "max_hops must be positive"
            )

        self.entity_resolver = LexicalEntityResolver(
            graph
        )
        self.path_enumerator = GraphPathEnumerator(
            graph
        )
        self.path_ranker = path_ranker
        self.max_hops = max_hops

    def answer(
        self,
        question: str,
    ) -> GraphQAResult:
        entity_resolution = (
            self.entity_resolver.resolve(
                question
            )
        )

        candidates = (
            self.path_enumerator.enumerate_literal_paths(
                start_entity_id=(
                    entity_resolution.entity_id
                ),
                max_hops=self.max_hops,
            )
        )

        if not candidates:
            raise ValueError(
                "resolved entity has no literal-valued paths "
                "within max_hops"
            )

        ranking = self.path_ranker.rank(
            question,
            candidates,
        )
        return self._build_result(
            question=question,
            entity_resolution=entity_resolution,
            ranking=ranking,
        )

    @staticmethod
    def _build_result(
        question: str,
        entity_resolution: EntityResolutionResult,
        ranking: list[RankedGraphPath],
    ) -> GraphQAResult:
        top = ranking[0]
        second_score = (
            float(ranking[1].score)
            if len(ranking) > 1
            else None
        )
        margin = (
            float(top.score) - second_score
            if second_score is not None
            else None
        )

        return GraphQAResult(
            question=question,
            entity_resolution=entity_resolution,
            relation_path=top.candidate.relation_path,
            claim_ids=top.candidate.claim_ids,
            answer=top.candidate.final_value,
            evidence=top.candidate.evidence,
            top_path_score=float(top.score),
            second_path_score=second_score,
            path_score_margin=margin,
            candidate_path_count=len(ranking),
        )
