"""EXP-123: same-tool static vs multi-step rule-agent evidence retrieval.

All arms receive the same search interface; the rule planner observes only
the top document text from each call. Gold labels are evaluator-only.
"""

from dataclasses import dataclass
from statistics import fmean
from typing import Protocol

from knowledge_engine.agent.actions import PlannerActionType
from knowledge_engine.agent.observation_parser import parse_retrieval_observation
from knowledge_engine.agent.rule_based_planner import RuleBasedPlanner
from knowledge_engine.agent.state import PlannerState
from knowledgebench.tasks.multihop_schema import MultiHopTask

TOP_K = 3
MAX_SEARCHES = 3
ARM_NAMES = ("static_top3", "static_top9", "static_repeat3", "rule_agent3")


class SearchBackend(Protocol):
    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]: ...


@dataclass(frozen=True)
class SearchTrace:
    task_id: str
    arm: str
    queries: tuple[str, ...]
    retrieved_per_call: tuple[tuple[str, ...], ...]
    observed_top1: tuple[str, ...]
    stopped: bool
    planner_failed: bool
    final_answer: str | None

    @property
    def calls(self) -> int:
        return len(self.queries)

    @property
    def all_retrieved_ids(self) -> set[str]:
        return {doc_id for call in self.retrieved_per_call for doc_id in call}


@dataclass(frozen=True)
class SearchGrade:
    task_id: str
    arm: str
    recall: float
    complete: bool
    calls: int
    unique_docs: int
    total_hits: int
    repeated_queries: int
    stopped: bool
    planner_failed: bool


def _search(
    backend: SearchBackend, query: str, k: int, valid_ids: set[str],
) -> tuple[str, ...]:
    ranked = backend.search(query, top_k=k)
    ids = tuple(doc_id for doc_id, _ in ranked)
    if len(ids) != len(set(ids)) or len(ids) > k or not set(ids).issubset(valid_ids):
        raise ValueError("invalid search output: duplicate, unknown or over-budget IDs")
    if not ids:
        raise ValueError("search returned no evidence")
    return ids


def run_arm(
    *,
    question: str,
    task_id: str,
    arm: str,
    backend: SearchBackend,
    document_texts: dict[str, str],
    planner: RuleBasedPlanner | None = None,
) -> SearchTrace:
    if arm not in ARM_NAMES:
        raise ValueError("unknown experimental arm")
    if not question.strip() or not document_texts:
        raise ValueError("question and corpus must be nonempty")
    valid_ids = set(document_texts)
    queries: list[str] = []
    returned: list[tuple[str, ...]] = []
    observed: list[str] = []
    stopped = False
    failed = False
    answer: str | None = None

    if arm != "rule_agent3":
        # static_top9 exposes nine results in ONE call, compared with up to
        # 3 calls x 3 hits for agent; repeat3 holds calls constant without
        # injecting target-specific or gold-derived query reformulations.
        repeat = MAX_SEARCHES if arm == "static_repeat3" else 1
        k = TOP_K * MAX_SEARCHES if arm == "static_top9" else TOP_K
        for _ in range(repeat):
            ids = _search(backend, question, k, valid_ids)
            queries.append(question)
            returned.append(ids)
            observed.append(ids[0])
    else:
        if planner is None:
            planner = RuleBasedPlanner()
        state = PlannerState(question=question)
        for _ in range(MAX_SEARCHES + 1):
            try:
                action = planner.next_action(state)
            except ValueError:
                failed = True
                break
            if action.action_type == PlannerActionType.STOP:
                stopped = True
                answer = action.answer
                break
            if len(queries) == MAX_SEARCHES:
                break
            if action.action_type != PlannerActionType.SEARCH or action.query is None:
                failed = True
                break
            query = action.query
            ids = _search(backend, query, TOP_K, valid_ids)
            queries.append(query)
            returned.append(ids)
            observed.append(ids[0])
            state.retrieval_state = parse_retrieval_observation(
                ids[0], document_texts[ids[0]]
            )
            state.step_index += 1

    return SearchTrace(
        task_id=task_id, arm=arm, queries=tuple(queries),
        retrieved_per_call=tuple(returned), observed_top1=tuple(observed),
        stopped=stopped, planner_failed=failed, final_answer=answer,
    )


def grade_traces(
    tasks: list[MultiHopTask], traces: list[SearchTrace],
) -> list[SearchGrade]:
    task_by_id = {task.task_id: task for task in tasks}
    if len(task_by_id) != len(tasks):
        raise ValueError("duplicate task IDs")
    expected = {(task.task_id, arm) for task in tasks for arm in ARM_NAMES}
    observed = [(trace.task_id, trace.arm) for trace in traces]
    if set(observed) != expected or len(observed) != len(expected):
        raise ValueError("missing, extra, or duplicate trace")
    graded = []
    for trace in traces:
        if trace.calls != len(trace.retrieved_per_call) or (
            trace.calls != len(trace.observed_top1)
        ):
            raise ValueError("malformed call trace")
        if any(not ids or top1 != ids[0] for ids, top1 in zip(
            trace.retrieved_per_call, trace.observed_top1
        )):
            raise ValueError("observation mismatch")
        if trace.arm in {"static_top3", "static_top9"} and trace.calls != 1:
            raise ValueError("static single-call budget violated")
        if trace.arm == "static_repeat3" and trace.calls != MAX_SEARCHES:
            raise ValueError("static repeat-call budget violated")
        if trace.arm == "rule_agent3" and trace.calls > MAX_SEARCHES:
            raise ValueError("agent call cap violated")
        if any(len(ids) > (9 if trace.arm == "static_top9" else TOP_K)
               for ids in trace.retrieved_per_call):
            raise ValueError("retrieval per-call cap violated")
        relevant = {hop.expected_document_id for hop in task_by_id[trace.task_id].hops}
        recovered = relevant & trace.all_retrieved_ids
        normalized = [query.strip().casefold() for query in trace.queries]
        graded.append(SearchGrade(
            task_id=trace.task_id, arm=trace.arm,
            recall=len(recovered) / len(relevant),
            complete=relevant.issubset(trace.all_retrieved_ids),
            calls=trace.calls, unique_docs=len(trace.all_retrieved_ids),
            total_hits=sum(len(ids) for ids in trace.retrieved_per_call),
            repeated_queries=len(normalized) - len(set(normalized)),
            stopped=trace.stopped, planner_failed=trace.planner_failed,
        ))
    return graded


def aggregate_grades(grades: list[SearchGrade]) -> dict[str, dict[str, float]]:
    if not grades:
        raise ValueError("no search grades")
    report: dict[str, dict[str, float]] = {}
    for arm in ARM_NAMES:
        rows = [row for row in grades if row.arm == arm]
        if not rows:
            raise ValueError("missing arm")
        report[arm] = {
            "recall": fmean(x.recall for x in rows),
            "complete_rate": fmean(float(x.complete) for x in rows),
            "mean_calls": fmean(x.calls for x in rows),
            "mean_unique_docs": fmean(x.unique_docs for x in rows),
            "mean_total_hits": fmean(x.total_hits for x in rows),
            "mean_repeated_queries": fmean(x.repeated_queries for x in rows),
            "planner_failure_rate": fmean(float(x.planner_failed) for x in rows),
            "stopped_rate": fmean(float(x.stopped) for x in rows),
        }
    return report
