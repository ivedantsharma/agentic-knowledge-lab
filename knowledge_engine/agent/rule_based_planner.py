import re

from knowledge_engine.agent.actions import (
    PlannerAction,
    PlannerActionType,
)
from knowledge_engine.agent.state import PlannerState


_FINAL_EVIDENCE_PATTERNS = (
    "incremental backups run",
    "retried at most",
    "cached for",
    "signing keys rotate",
)


class RuleBasedPlanner:
    """Deterministic planner that does not read benchmark hop labels."""

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

        query = self._next_query(state)

        return PlannerAction(
            action_type=PlannerActionType.SEARCH,
            query=query,
        )

    def _next_query(
        self,
        state: PlannerState,
    ) -> str:
        question = state.question
        retrieval_state = state.retrieval_state
        entity = retrieval_state.entity
        evidence = (
            retrieval_state.evidence_text
            or ""
        )
        qualifier = (
            retrieval_state.qualifiers[0]
            if retrieval_state.qualifiers
            else None
        )

        if entity is None:
            operates_match = re.search(
                r"team that operates ([A-Za-z0-9_-]+)",
                question,
                flags=re.IGNORECASE,
            )

            if operates_match is not None:
                service = operates_match.group(1)
                return (
                    f"Which team operates {service}?"
                )

            worker_match = re.search(
                r"worker platform maintained by (.+?)[?]?$",
                question,
                flags=re.IGNORECASE,
            )

            if worker_match is not None:
                team = worker_match.group(1).strip()
                return (
                    "Which worker platform is maintained by "
                    f"{team}?"
                )

            signing_match = re.search(
                r"signing service maintained by (.+?)[?]?$",
                question,
                flags=re.IGNORECASE,
            )

            if signing_match is not None:
                team = signing_match.group(1).strip()
                return (
                    "Which signing service is maintained by "
                    f"{team}?"
                )

            raise ValueError(
                "rule-based planner cannot form initial query"
            )

        evidence_lower = evidence.casefold()

        if "operated by" in evidence_lower:
            if "storage system" in question.casefold():
                return (
                    "Which storage system is maintained by "
                    f"{entity}?"
                )

            if "cache duration" in question.casefold():
                return (
                    "Which cache service is maintained by "
                    f"{entity}?"
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
            "rule-based planner cannot determine next search"
        )
