from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.entity_resolution import (
    EntityResolutionResult,
    LexicalEntityResolver,
)
from knowledge_engine.graph.entity_type import (
    FirstCueEntityTypeInferer,
)
from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
)


class HybridEntityResolver:
    """Prefer lexical linking, then use typed semantic fallback."""

    def __init__(
        self,
        graph: ClaimGraph,
        model_name: str,
        threshold: float,
        model: SentenceTransformer | None = None,
    ) -> None:
        self.lexical = LexicalEntityResolver(
            graph
        )
        self.type_inferer = (
            FirstCueEntityTypeInferer()
        )
        self.semantic = SemanticEntityRanker(
            graph=graph,
            model_name=model_name,
            model=model,
        )
        self.threshold = threshold

    def resolve(
        self,
        question: str,
    ) -> EntityResolutionResult:
        try:
            return self.lexical.resolve(
                question
            )
        except ValueError:
            pass

        type_result = self.type_inferer.infer(
            question
        )
        if type_result.entity_type is None:
            raise ValueError(
                "unable to infer entity type for semantic fallback"
            )

        ranking = self.semantic.rank_for_type(
            question,
            type_result.entity_type,
        )
        top = ranking[0]

        if top.score < self.threshold:
            raise ValueError(
                "semantic entity score below threshold: "
                f"{top.score:.6f} < {self.threshold:.6f}"
            )

        return EntityResolutionResult(
            entity_id=top.entity_id,
            matched_surface=question,
            match_type=(
                "semantic_"
                f"{type_result.entity_type}"
            ),
        )
