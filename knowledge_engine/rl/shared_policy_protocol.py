"""EXP-124 Gate B0: versioned common decision protocol for FUTURE SFT/RL.

This is a mechanics contract, not learned-model inference. Both new policies
must consume the same RetrievalObservation, select one legal RetrievalRLAction,
and run in the same RetrievalEpisodeV2 with a fixed external ranking.
Historical Phase 11 REFORMULATE and Hybrid policy actions are NOT cast.
"""

from dataclasses import dataclass
from typing import Protocol

from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisodeV2,
    RetrievalObservation,
    RetrievalRLAction,
)
from knowledge_engine.rl.stochastic_policy import legal_actions
from knowledge_engine.rl.trajectory_baselines import discounted_return

PROTOCOL_ID = "EXP-124-common-bm25-v0"
ACTION_NAMES = tuple(action.value for action in RetrievalRLAction)
MAX_STEPS = 6
GAMMA = 0.9


class ActionPolicy(Protocol):
    """Both newly trained policy types must implement this exact interface."""

    def choose_action(self, observation: RetrievalObservation) -> RetrievalRLAction: ...


@dataclass(frozen=True)
class FixedKPolicy:
    """Gold-blind baseline under the same action mask and stopping rules."""

    k: int

    def __post_init__(self) -> None:
        if self.k not in (1, 2, 3, 5):
            raise ValueError("fixed policy K must be one of 1,2,3,5")

    def choose_action(self, observation: RetrievalObservation) -> RetrievalRLAction:
        if observation.requested_k > 0:
            return RetrievalRLAction.STOP
        return RetrievalRLAction(f"SEARCH_K{self.k}")


@dataclass(frozen=True)
class SharedEpisodeResult:
    protocol_id: str
    actions: tuple[RetrievalRLAction, ...]
    rewards: tuple[float, ...]
    final_observation: RetrievalObservation
    discounted_return: float

    @property
    def documents_returned(self) -> int:
        return len(self.final_observation.retrieved_ids)


def run_shared_episode(
    *,
    policy: ActionPolicy,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    max_steps: int = MAX_STEPS,
) -> SharedEpisodeResult:
    """Only observation is passed to policy; gold enters episode reward only.

    Preconditions: the ranking is computed by the shared BM25 engine with
    the same frozen documents and query. Future data ingestion must enforce
    that source provenance; this adapter cannot verify its caller's ranker.
    """
    episode = RetrievalEpisodeV2(
        question=question,
        ranked_ids=ranked_ids,
        supporting_ids=supporting_ids,
        max_steps=max_steps,
    )
    actions: list[RetrievalRLAction] = []
    rewards: list[float] = []
    while not episode.observe().done:
        observation = episode.observe()
        action = policy.choose_action(observation)
        if not isinstance(action, RetrievalRLAction):
            raise ValueError("policy returned non-contract action")
        if action not in legal_actions(observation):
            raise ValueError(f"policy returned illegal action: {action}")
        transition = episode.step(action)
        actions.append(action)
        rewards.append(transition.reward)
    return SharedEpisodeResult(
        protocol_id=PROTOCOL_ID,
        actions=tuple(actions),
        rewards=tuple(rewards),
        final_observation=episode.observe(),
        discounted_return=discounted_return(rewards, gamma=GAMMA),
    )
