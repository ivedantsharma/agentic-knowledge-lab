"""Phase 14 evidence-first integrated search with safe planner fallback.

No benchmark gold is an input. This pipeline deliberately does NOT generate
answers: retrieved text (even an apparently correct fact) is not verified.
Risk labels here come from document SOURCE METADATA, not benchmark labels.
"""

from dataclasses import dataclass

from knowledge_engine.agent.actions import PlannerActionType
from knowledge_engine.agent.observation_parser import parse_retrieval_observation
from knowledge_engine.agent.rule_based_planner import RuleBasedPlanner
from knowledge_engine.agent.state import PlannerState
from knowledge_engine.integrated.backends import RankingBackend, create_ranking_backend
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document

RISK_SOURCE_TYPES = {
    "service_manual_previous_revision": "previous_revision",
    "pending_policy_revision": "pending_revision",
}


@dataclass(frozen=True)
class EvidenceHit:
    document_id: str
    title: str
    text: str
    source_type: str
    effective_at: str | None
    risk_flag: str | None


@dataclass(frozen=True)
class SearchStep:
    query: str
    returned_document_ids: tuple[str, ...]


@dataclass(frozen=True)
class IntegratedResult:
    question: str
    strategy_requested: str
    strategy_used: str
    fallback_reason: str | None
    planner_stopped: bool
    steps: tuple[SearchStep, ...]
    evidence: tuple[EvidenceHit, ...]
    status: str
    answer: None

    def as_dict(self) -> dict[str, object]:
        return {
            "question": self.question,
            "strategy_requested": self.strategy_requested,
            "strategy_used": self.strategy_used,
            "fallback_reason": self.fallback_reason,
            "planner_stopped": self.planner_stopped,
            "steps": [
                {"query": step.query, "returned_document_ids": list(step.returned_document_ids)}
                for step in self.steps
            ],
            "evidence": [
                {
                    "document_id": item.document_id,
                    "title": item.title,
                    "text": item.text,
                    "source_type": item.source_type,
                    "effective_at": item.effective_at,
                    "risk_flag": item.risk_flag,
                }
                for item in self.evidence
            ],
            "status": self.status,
            "answer": None,
        }


class IntegratedKnowledgeEngine:
    """Execute one fixed lexical retriever and optional dependent searches.

    `auto` attempts the historic rule planner; unsupported intents fall back
    to an unchanged-question BM25 search rather than an empty result.
    Planner observations are top-1 only, never benchmark answer labels.
    """

    def __init__(
        self,
        documents: list[KnowledgeBenchV2Document],
        *,
        planner: RuleBasedPlanner | None = None,
        backend: RankingBackend | None = None,
    ) -> None:
        if not documents or len({doc.document_id for doc in documents}) != len(documents):
            raise ValueError("documents must be nonempty with unique IDs")
        self._documents = {doc.document_id: doc for doc in documents}
        self._retriever = backend if backend is not None else create_ranking_backend(documents)
        self._planner = planner if planner is not None else RuleBasedPlanner()

    def query(
        self,
        question: str,
        *,
        strategy: str = "auto",
        top_k: int = 3,
        max_planner_searches: int = 3,
    ) -> IntegratedResult:
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty")
        if strategy not in {"auto", "static", "planner"}:
            raise ValueError("strategy must be auto, static or planner")
        if top_k < 1 or top_k > len(self._documents):
            raise ValueError("top_k out of range")
        if not 1 <= max_planner_searches <= 6:
            raise ValueError("max_planner_searches must be within 1..6")
        steps: list[SearchStep] = []
        seen_ids: dict[str, None] = {}
        stopped = False
        fallback: str | None = None

        def search(query: str) -> tuple[str, ...]:
            ranked = self._retriever.rank(query, top_k)
            ids = tuple(item_id for item_id, _ in ranked)
            if (
                len(ids) > top_k
                or len(ids) != len(set(ids))
                or not set(ids).issubset(self._documents)
            ):
                raise ValueError("backend returned duplicate, unknown or over-budget IDs")
            steps.append(SearchStep(query=query, returned_document_ids=ids))
            for item_id in ids:
                seen_ids[item_id] = None
            return ids

        if strategy == "static":
            search(question)
            used = "static"
        else:
            state = PlannerState(question=question)
            used = "planner"
            for _ in range(max_planner_searches + 1):
                try:
                    action = self._planner.next_action(state)
                except ValueError:
                    fallback = "planner_query_unsupported"
                    break
                if action.action_type == PlannerActionType.STOP:
                    stopped = True
                    break
                if len(steps) >= max_planner_searches:
                    fallback = "planner_search_budget_exhausted"
                    break
                if action.action_type != PlannerActionType.SEARCH or not action.query:
                    fallback = "planner_invalid_action"
                    break
                ids = search(action.query)
                if not ids:
                    fallback = "planner_no_results"
                    break
                state.retrieval_state = parse_retrieval_observation(
                    ids[0], self._documents[ids[0]].text
                )
                state.step_index += 1
            if fallback is not None or not steps:
                search(question)
                used = "planner_with_static_fallback"

        evidence = tuple(
            EvidenceHit(
                document_id=item_id,
                title=doc.title,
                text=doc.text,
                source_type=doc.source_type,
                effective_at=doc.effective_at,
                risk_flag=RISK_SOURCE_TYPES.get(doc.source_type),
            )
            for item_id in seen_ids
            for doc in (self._documents[item_id],)
        )
        return IntegratedResult(
            question=question,
            strategy_requested=strategy,
            strategy_used=used,
            fallback_reason=fallback,
            planner_stopped=stopped,
            steps=tuple(steps),
            evidence=evidence,
            status="evidence_only_unverified",
            answer=None,
        )
