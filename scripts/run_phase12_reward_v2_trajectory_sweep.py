"""EXP-114: deterministic reward v2 termination/trajectory invariants.

Only the grounded Cirrus case uses benchmark gold labels. Synthetic cases
probe edge conditions and must not be reported as benchmark performance.
"""

import json
import sys
from dataclasses import dataclass
from itertools import combinations
from math import isclose
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.reward_audit import RewardAudit, audit_trajectory
from knowledge_engine.rl.retrieval_environment import RetrievalRLAction

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/phase10_routing_pairs_v0.json")
RANKING = (
    "kbv2-doc-cirrus-contradiction",
    "kbv2-doc-cirrus-manual",
    "kbv2-doc-cumulus-retry",
    "kbv2-doc-cirrus-org",
    "kbv2-doc-borealis-stale",
)
SEARCH_ACTIONS = (
    RetrievalRLAction.SEARCH_K1,
    RetrievalRLAction.SEARCH_K2,
    RetrievalRLAction.SEARCH_K3,
    RetrievalRLAction.SEARCH_K5,
)


@dataclass(frozen=True)
class AuditCase:
    name: str
    question: str
    ranked_ids: tuple[str, ...]
    supporting_ids: frozenset[str]
    conflicting_ids: frozenset[str]
    synthetic: bool


@dataclass(frozen=True)
class SweepResult:
    case_name: str
    actions: tuple[RetrievalRLAction, ...]
    v1_timeout: RewardAudit
    v2_timeout: RewardAudit
    v2_stop: RewardAudit


def cases(question: str, cirrus_supporting_ids: frozenset[str]) -> tuple[AuditCase, ...]:
    """Preserve actual gold on Cirrus; mark all changed-label probes synthetic."""
    return (
        AuditCase(
            "cirrus_grounded", question, RANKING, cirrus_supporting_ids,
            frozenset({RANKING[0]}), False,
        ),
        AuditCase(
            "synthetic_two_support", question, RANKING,
            frozenset({RANKING[1], RANKING[3]}), frozenset({RANKING[0]}), True,
        ),
        AuditCase(
            "synthetic_late_support", question, RANKING,
            frozenset({RANKING[4]}), frozenset({RANKING[0]}), True,
        ),
        AuditCase(
            "synthetic_out_of_budget", question, (*RANKING, "synthetic-sixth-doc"),
            frozenset({"synthetic-sixth-doc"}), frozenset({RANKING[0]}), True,
        ),
    )


def increasing_search_prefixes() -> tuple[tuple[RetrievalRLAction, ...], ...]:
    """All 15 nonempty strictly increasing action-budget subsequences."""
    return tuple(
        seq
        for length in range(1, len(SEARCH_ACTIONS) + 1)
        for seq in combinations(SEARCH_ACTIONS, length)
    )


def sweep_case(case: AuditCase) -> list[SweepResult]:
    """Compare a forced timeout against STOP after the *identical* prefix."""
    results = []
    common = dict(
        question=case.question,
        ranked_ids=list(case.ranked_ids),
        supporting_ids=set(case.supporting_ids),
        conflicting_ids=set(case.conflicting_ids),
    )
    for prefix in increasing_search_prefixes():
        timeout_kwargs = dict(common, actions=list(prefix), max_steps=len(prefix))
        v1, v1_transitions = audit_trajectory(**timeout_kwargs, reward_version="v1")
        v2, v2_transitions = audit_trajectory(**timeout_kwargs, reward_version="v2")
        stop, stop_transitions = audit_trajectory(
            **common,
            actions=[*prefix, RetrievalRLAction.STOP],
            max_steps=len(prefix) + 1,
            reward_version="v2",
        )
        assert v1.terminal_without_stop and v2.terminal_without_stop
        assert stop.stopped_explicitly and not stop.terminal_without_stop
        assert len(v1_transitions) == len(v2_transitions) == len(prefix)
        assert len(stop_transitions) == len(prefix) + 1
        assert v1.coverage == v2.coverage == stop.coverage
        assert (
            v1.conflicting_exposure_count
            == v2.conflicting_exposure_count
            == stop.conflicting_exposure_count
        )
        assert v1.retrieval_cost_count == v2.retrieval_cost_count == stop.retrieval_cost_count
        # Gold labels remain exclusively in evaluator state, not observations.
        assert all(
            not hasattr(t.next_observation, "supporting_ids")
            for t in v2_transitions
        )
        incomplete = v2.coverage < 1.0
        expected_delta = -1.0 if incomplete else 0.0
        assert isclose(v2.total_reward - v1.total_reward, expected_delta, abs_tol=1e-9)
        expected_stop_advantage = 0.0 if incomplete else 1.0
        assert isclose(
            stop.total_reward - v2.total_reward, expected_stop_advantage, abs_tol=1e-9
        )
        assert all(t.new_document_count >= 0 and t.new_support_count >= 0 for t in v2_transitions)
        assert sum(t.new_document_count for t in v2_transitions) == v2.retrieval_cost_count
        results.append(SweepResult(case.name, prefix, v1, v2, stop))
    return results


def main() -> None:
    documents = json.loads(DOCS.read_text(encoding="utf-8"))
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))
    by_id = {doc["document_id"]: doc for doc in documents}
    task = next(t for t in tasks if t["task_id"] == "route-003")
    assert set(RANKING).issubset(by_id)
    assert by_id[RANKING[0]]["source_type"] == "pending_policy_revision"
    assert by_id[RANKING[1]]["source_type"] == "service_manual"
    assert set(task["supporting_document_ids"]) == {RANKING[1]}
    print("Phase 12 EXP-114 — Reward v2 Trajectory-Wide Validation")
    print("Frozen Cirrus ranking; synthetic stress cases clearly distinguished.")
    print("Counterfactual STOP always follows the same retrieval prefix as timeout.")
    print()

    total = 0
    for case in cases(task["question"], frozenset(task["supporting_document_ids"])):
        results = sweep_case(case)
        incomplete = sum(r.v2_timeout.coverage < 1.0 for r in results)
        complete = len(results) - incomplete
        partial = sum(0.0 < r.v2_timeout.coverage < 1.0 for r in results)
        conflicts = sum(r.v2_timeout.conflicting_exposure_count > 0 for r in results)
        total += len(results)
        label = "synthetic" if case.synthetic else "grounded"
        print(
            f"{case.name} ({label}): prefixes={len(results)} "
            f"incomplete={incomplete} complete={complete} "
            f"partial_coverage={partial} conflict_exposed={conflicts}"
        )
    print()
    print(f"PASS: {total} timeout/STOP counterfactual pairs validated.")
    print("Invariant: incomplete v2 timeout = explicit premature STOP after same prefix.")
    print("Invariant: complete v2 timeout retains v1 reward; complete STOP gains +1.")
    print("Limit: synthetic probes are not benchmark accuracy results or trained RL evidence.")
    print("Limit: max retrieval budget K=5 cannot complete the sixth-document probe.")


if __name__ == "__main__":
    main()
