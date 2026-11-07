import re

from sentence_transformers import SentenceTransformer

from knowledge_engine.agent.actions import (
    PlannerAction,
    PlannerActionType,
)
from knowledge_engine.agent.state import PlannerState
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledgebench.documents.schema import KnowledgeDocument

_GOAL_PROTOTYPES = {
    "backup": (
        "What is the incremental backup cadence of a storage system?"
    ),
    "retry": (
        "How many times are failed jobs retried on a worker platform?"
    ),
    "cache": (
        "How long is validated session metadata cached?"
    ),
    "signing": (
        "How often do signing keys rotate for a signing service?"
    ),
}

_FINAL_EVIDENCE_PATTERNS = (
    "incremental backups run",
    "retried at most",
    "cached for",
    "signing keys rotate",
)


class SemanticPlanner:
    """Embedding-backed planner baseline for paraphrased questions."""

    def __init__(
        self,
        documents: list[KnowledgeDocument],
        model_name: str,
        model: SentenceTransformer | None = None,
    ) -> None:
        self.model = (
            model
            if model is not None
            else SentenceTransformer(model_name)
        )

        self.goal_names = list(_GOAL_PROTOTYPES)
        self.goal_embeddings = self.model.encode(
            [
                _GOAL_PROTOTYPES[name]
                for name in self.goal_names
            ]
        )

        self.known_entities = self._discover_entities(
            documents
        )

    def next_action(
        self,
        state: PlannerState,
    ) -> PlannerAction:
        evidence = (
            state.retrieval_state.evidence_text
            or ""
        )

        if (
            state.retrieval_state.entity is not None
            and any(
                marker in evidence.casefold()
                for marker in _FINAL_EVIDENCE_PATTERNS
            )
        ):
            return PlannerAction(
                action_type=PlannerActionType.STOP,
                answer=state.retrieval_state.entity,
            )

        goal = self.classify_goal(
            state.question
        )

        query = self._next_query(
            state,
            goal,
        )

        return PlannerAction(
            action_type=PlannerActionType.SEARCH,
            query=query,
        )

    def classify_goal(
        self,
        question: str,
    ) -> str:
        question_embedding = self.model.encode(
            question
        ).tolist()

        scores = [
            cosine_similarity(
                question_embedding,
                embedding.tolist(),
            )
            for embedding in self.goal_embeddings
        ]

        best_index = max(
            range(len(scores)),
            key=scores.__getitem__,
        )

        return self.goal_names[best_index]

    def find_anchor_entity(
        self,
        question: str,
    ) -> str | None:
        question_lower = question.casefold()

        matches = [
            entity
            for entity in self.known_entities
            if entity.casefold() in question_lower
        ]

        if not matches:
            return None

        return max(
            matches,
            key=len,
        )

    def _next_query(
        self,
        state: PlannerState,
        goal: str,
    ) -> str:
        retrieval_state = state.retrieval_state
        entity = retrieval_state.entity
        evidence = (
            retrieval_state.evidence_text
            or ""
        )

        if entity is None:
            anchor = self.find_anchor_entity(
                state.question
            )

            if anchor is None:
                raise ValueError(
                    "semantic planner cannot find anchor entity"
                )

            if goal in {"backup", "cache"}:
                return (
                    f"Which team operates {anchor}?"
                )

            if goal == "retry":
                return (
                    "Which worker platform is maintained by "
                    f"{anchor}?"
                )

            if goal == "signing":
                return (
                    "Which signing service is maintained by "
                    f"{anchor}?"
                )

        evidence_lower = evidence.casefold()

        if "operated by" in evidence_lower:
            if goal == "backup":
                return (
                    "Which storage system is maintained by "
                    f"{entity}?"
                )

            if goal == "cache":
                return (
                    "Which cache service is maintained by "
                    f"{entity}?"
                )

        qualifier = (
            retrieval_state.qualifiers[0]
            if retrieval_state.qualifiers
            else None
        )
        prefix = (
            f"{qualifier} "
            if qualifier is not None
            else ""
        )

        if "storage system" in evidence_lower:
            return (
                "What is the incremental backup cadence for "
                f"the {prefix}{entity} service?"
            )

        if "worker platform" in evidence_lower:
            return (
                "How many times are failed jobs retried by "
                f"the {prefix}{entity} worker platform?"
            )

        if "cache service" in evidence_lower:
            return (
                "How long is metadata cached by the "
                f"{prefix}{entity} cache service?"
            )

        if "signing service" in evidence_lower:
            return (
                "How often do signing keys rotate for the "
                f"{prefix}{entity} signing service?"
            )

        raise ValueError(
            "semantic planner cannot determine next search"
        )

    @staticmethod
    def _discover_entities(
        documents: list[KnowledgeDocument],
    ) -> list[str]:
        patterns = (
            r"^(.+?) is operated by",
            r"^(.+?) maintains",
        )

        entities: set[str] = set()

        for document in documents:
            for pattern in patterns:
                match = re.search(
                    pattern,
                    document.text,
                    flags=re.IGNORECASE,
                )

                if match is not None:
                    entities.add(
                        match.group(1).strip()
                    )
                    break

        return sorted(entities)
