"""Finite-horizon return and oracle baselines for Phase 12.

Oracle selection uses hidden gold labels exclusively for *evaluation*.
None of these functions provides gold labels to a deployable policy.
"""

from dataclasses import dataclass
from itertools import combinations
from math import isfinite
from typing import Iterable

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.rl.reward_audit import RewardAudit, audit_trajectory

SEARCH_ACTIONS = (
    RetrievalRLAction.SEARCH_K1,
    RetrievalRLAction.SEARCH_K2,
    RetrievalRLAction.SEARCH_K3,
    RetrievalRLAction.SEARCH_K5,
)


@dataclass(frozen=True)
class TrajectoryScore:
    actions: tuple[RetrievalRLAction, ...]
    rewards: tuple[float, ...]
    report: RewardAudit
    discounted_return: float


def discounted_return(rewards: Iterable[float], *, gamma: float = 1.0) -> float:
    """G_0 = sum_t gamma**t * r_t for an episode starting at time zero."""
    if not isfinite(gamma) or not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must be finite and in [0, 1]")
    return sum((gamma**t) * reward for t, reward in enumerate(rewards))


def legal_terminated_trajectories(
    *, max_steps: int = 6
) -> tuple[tuple[RetrievalRLAction, ...], ...]:
    """All legal terminal paths under strictly increasing retrieval budgets.

    A path ends via explicit STOP, or via forced timeout on the last step.
    """
    if max_steps < 1:
        raise ValueError("max_steps must be positive")
    search_prefixes = (
        (), *(
            prefix
            for size in range(1, len(SEARCH_ACTIONS) + 1)
            for prefix in combinations(SEARCH_ACTIONS, size)
        )
    )
    paths = []
    for prefix in search_prefixes:
        if len(prefix) < max_steps:
            paths.append((*prefix, RetrievalRLAction.STOP))
        elif len(prefix) == max_steps:
            paths.append(prefix)
    return tuple(paths)


def score_trajectory(
    *,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    conflicting_ids: set[str],
    actions: tuple[RetrievalRLAction, ...],
    gamma: float = 1.0,
    max_steps: int = 6,
) -> TrajectoryScore:
    """Evaluate a full episode; labels are passed to the evaluator only."""
    # Validate gamma even on trajectories with no rewards.
    discounted_return((), gamma=gamma)
    report, transitions = audit_trajectory(
        question=question,
        ranked_ids=ranked_ids,
        supporting_ids=supporting_ids,
        conflicting_ids=conflicting_ids,
        actions=list(actions),
        max_steps=max_steps,
        reward_version="v2",
    )
    if not report.episode_done:
        raise ValueError("trajectory must terminate with STOP or a timeout")
    rewards = tuple(transition.reward for transition in transitions)
    return TrajectoryScore(
        actions=actions,
        rewards=rewards,
        report=report,
        discounted_return=discounted_return(rewards, gamma=gamma),
    )


def oracle_trajectory(
    *,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    conflicting_ids: set[str],
    gamma: float = 1.0,
    max_steps: int = 6,
) -> TrajectoryScore:
    """Gold-aware diagnostic upper bound, never an executable learned policy."""
    options = [
        score_trajectory(
            question=question,
            ranked_ids=ranked_ids,
            supporting_ids=supporting_ids,
            conflicting_ids=conflicting_ids,
            actions=actions,
            gamma=gamma,
            max_steps=max_steps,
        )
        for actions in legal_terminated_trajectories(max_steps=max_steps)
    ]
    return min(
        options,
        key=lambda item: (
            -round(item.discounted_return, 12),
            item.report.retrieval_cost_count,
            len(item.actions),
            tuple(action.value for action in item.actions),
        ),
    )


def fixed_policy_actions() -> dict[str, tuple[RetrievalRLAction, ...]]:
    """No gold-dependent action choices: explicit deployable fixed policies."""
    return {
        "STOP_NOW": (RetrievalRLAction.STOP,),
        "FIXED_K1": (RetrievalRLAction.SEARCH_K1, RetrievalRLAction.STOP),
        "FIXED_K2": (RetrievalRLAction.SEARCH_K2, RetrievalRLAction.STOP),
        "FIXED_K3": (RetrievalRLAction.SEARCH_K3, RetrievalRLAction.STOP),
        "FIXED_K5": (RetrievalRLAction.SEARCH_K5, RetrievalRLAction.STOP),
        "ESCALATE": (
            RetrievalRLAction.SEARCH_K1,
            RetrievalRLAction.SEARCH_K2,
            RetrievalRLAction.SEARCH_K3,
            RetrievalRLAction.SEARCH_K5,
            RetrievalRLAction.STOP,
        ),
    }
