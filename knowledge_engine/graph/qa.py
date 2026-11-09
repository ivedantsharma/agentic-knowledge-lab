from dataclasses import dataclass

from sentence_transformers import SentenceTransformer

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
from knowledge_engine.graph.traversal import (
    ClaimGraphIndex,
)


@dataclass(frozen=True)
class GraphQAResult:
    entity_resolution: EntityResolutionResult
    selected_path: RankedGraphPath
    final_value: str
    claim_ids: list[str]
    evidence: list[EvidenceReference]


class GraphQAPipeline:
    """Natural-language entry point for lexical entity linking + graph path ranking."""

    def __init__(
        self,
        graph: ClaimGraph,
        model_name: str,
        model: SentenceTransformer | None = None,
        max_hops: int = 3,
    ) -> None:
        if max_hops <= 0:
            raise ValueError(
                "max_hops must be positive"
            )

        self.graph = graph
        self.max_hops = max_hops
        self.entity_resolver = LexicalEntityResolver(
            graph
        )
        self.path_enumerator = GraphPathEnumerator(
            graph
        )
        self.path_ranker = SemanticGraphPathRanker(
            model_name=model_name,
            model=model,
        )
        self.graph_index = ClaimGraphIndex(
            graph
        )

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

        ranking = self.path_ranker.rank(
            question,
            candidates,
        )
        selected_path = ranking[0]

        traversal = self.graph_index.traverse(
            start_entity_id=(
                entity_resolution.entity_id
            ),
            relation_path=(
                selected_path.candidate.relation_path
            ),
        )

        return GraphQAResult(
            entity_resolution=entity_resolution,
            selected_path=selected_path,
            final_value=traversal.final_value,
            claim_ids=traversal.claim_ids,
            evidence=traversal.evidence,
        )
