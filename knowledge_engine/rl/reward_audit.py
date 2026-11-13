"""Evaluator-only Phase 12 reward audit; never use these signals as policy features."""

from dataclasses import dataclass

from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisode,
    RetrievalRLAction,
    RetrievalTransition,
    total_return,
)


@dataclass(frozen=True)
class RewardAudit:
    total_reward: float
    coverage: float
    retrieval_cost_count: int
    conflicting_exposure_count: int
    episode_done: bool
    stopped_explicitly: bool
    terminal_without_stop: bool


def audit_trajectory(
    *,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    conflicting_ids: set[str],
    actions: list[RetrievalRLAction],
    max_steps: int = 6,
    cost_per_document: float = 0.1,
) -> tuple[RewardAudit, list[RetrievalTransition]]:
    """Audit reward versus evidence/risk/termination using hidden gold labels."""
    if not conflicting_ids.issubset(set(ranked_ids)):
        raise ValueError("conflicting IDs must exist in ranking")
    episode = RetrievalEpisode(
        question,
        ranked_ids,
        supporting_ids,
        max_steps=max_steps,
        cost_per_document=cost_per_document,
    )
    transitions = [episode.step(action) for action in actions]
    observation = episode.observe()
    retrieved = set(observation.retrieved_ids)
    report = RewardAudit(
        total_reward=total_return(transitions),
        coverage=len(retrieved & supporting_ids) / len(supporting_ids),
        retrieval_cost_count=len(retrieved),
        conflicting_exposure_count=len(retrieved & conflicting_ids),
        episode_done=observation.done,
        stopped_explicitly=bool(
            transitions and transitions[-1].action == RetrievalRLAction.STOP
        ),
        terminal_without_stop=bool(
            observation.done
            and transitions
            and transitions[-1].action != RetrievalRLAction.STOP
        ),
    )
    return report, transitions
