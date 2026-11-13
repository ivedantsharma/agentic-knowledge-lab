"""Deterministic retrieval environment for Phase 12 reward studies.

Gold supporting IDs remain inside the environment/evaluator and are never
included in the policy-visible observation.
"""

from dataclasses import dataclass
from enum import StrEnum


class RetrievalRLAction(StrEnum):
    SEARCH_K1 = "SEARCH_K1"
    SEARCH_K2 = "SEARCH_K2"
    SEARCH_K3 = "SEARCH_K3"
    SEARCH_K5 = "SEARCH_K5"
    STOP = "STOP"


_BUDGETS = {
    RetrievalRLAction.SEARCH_K1: 1,
    RetrievalRLAction.SEARCH_K2: 2,
    RetrievalRLAction.SEARCH_K3: 3,
    RetrievalRLAction.SEARCH_K5: 5,
}


@dataclass(frozen=True)
class RetrievalObservation:
    question: str
    retrieved_ids: tuple[str, ...]
    requested_k: int
    steps_taken: int
    done: bool


@dataclass(frozen=True)
class RetrievalTransition:
    observation: RetrievalObservation
    action: RetrievalRLAction
    reward: float
    next_observation: RetrievalObservation
    new_document_count: int
    new_support_count: int


class RetrievalEpisode:
    """One fixed-ranking episode; labels are reserved for the evaluator."""

    def __init__(
        self,
        question: str,
        ranked_ids: list[str],
        supporting_ids: set[str],
        *,
        reward_per_support: float = 2.0,
        cost_per_document: float = 0.1,
        complete_stop_reward: float = 1.0,
        premature_stop_penalty: float = 1.0,
        max_steps: int = 6,
        timeout_incomplete_penalty: float = 0.0,
    ) -> None:
        if not question.strip() or not ranked_ids or not supporting_ids:
            raise ValueError("question, ranked_ids and supporting_ids must be nonempty")
        if len(set(ranked_ids)) != len(ranked_ids):
            raise ValueError("ranked_ids must contain unique document IDs")
        if not supporting_ids.issubset(set(ranked_ids)):
            raise ValueError("all supporting IDs must exist in the ranking")
        if max_steps < 1:
            raise ValueError("max_steps must be positive")
        self._question = question
        self._ranked_ids = tuple(ranked_ids)
        self._supporting_ids = frozenset(supporting_ids)
        self._reward_per_support = reward_per_support
        self._cost_per_document = cost_per_document
        self._complete_stop_reward = complete_stop_reward
        self._premature_stop_penalty = premature_stop_penalty
        self._max_steps = max_steps
        self._timeout_incomplete_penalty = timeout_incomplete_penalty
        self._retrieved_ids: tuple[str, ...] = ()
        self._requested_k = 0
        self._steps_taken = 0
        self._done = False

    def observe(self) -> RetrievalObservation:
        return RetrievalObservation(
            question=self._question,
            retrieved_ids=self._retrieved_ids,
            requested_k=self._requested_k,
            steps_taken=self._steps_taken,
            done=self._done,
        )

    def step(self, action: RetrievalRLAction) -> RetrievalTransition:
        if self._done:
            raise ValueError("episode already ended")
        if not isinstance(action, RetrievalRLAction):
            action = RetrievalRLAction(action)
        before = self.observe()
        newly_retrieved = 0
        new_support = 0
        if action == RetrievalRLAction.STOP:
            complete = self._supporting_ids.issubset(set(self._retrieved_ids))
            reward = (
                self._complete_stop_reward
                if complete
                else -self._premature_stop_penalty
            )
            self._done = True
        else:
            next_k = _BUDGETS[action]
            if next_k <= self._requested_k:
                raise ValueError("search budget must strictly increase")
            next_ids = tuple(self._ranked_ids[:next_k])
            newly_retrieved = len(next_ids) - len(self._retrieved_ids)
            new_support = len(
                (set(next_ids) - set(self._retrieved_ids))
                & self._supporting_ids
            )
            reward = (
                self._reward_per_support * new_support
                - self._cost_per_document * newly_retrieved
            )
            self._retrieved_ids = next_ids
            self._requested_k = next_k
        self._steps_taken += 1
        if self._steps_taken >= self._max_steps:
            # The original v1 reward has no timeout penalty (default zero).
            # Reward v2 charges incomplete forced termination like early STOP.
            if (
                action != RetrievalRLAction.STOP
                and not self._supporting_ids.issubset(set(self._retrieved_ids))
            ):
                reward -= self._timeout_incomplete_penalty
            self._done = True
        return RetrievalTransition(
            observation=before,
            action=action,
            reward=reward,
            next_observation=self.observe(),
            new_document_count=newly_retrieved,
            new_support_count=new_support,
        )


def total_return(transitions: list[RetrievalTransition]) -> float:
    return sum(transition.reward for transition in transitions)


class RetrievalEpisodeV2(RetrievalEpisode):
    """Reward v2: charge incomplete forced termination as premature STOP.

    Gold labels remain hidden from policy observations. Conflict exposure is
    deliberately audited separately rather than penalized automatically.
    """

    def __init__(
        self,
        question: str,
        ranked_ids: list[str],
        supporting_ids: set[str],
        *,
        reward_per_support: float = 2.0,
        cost_per_document: float = 0.1,
        complete_stop_reward: float = 1.0,
        premature_stop_penalty: float = 1.0,
        max_steps: int = 6,
    ) -> None:
        super().__init__(
            question=question,
            ranked_ids=ranked_ids,
            supporting_ids=supporting_ids,
            reward_per_support=reward_per_support,
            cost_per_document=cost_per_document,
            complete_stop_reward=complete_stop_reward,
            premature_stop_penalty=premature_stop_penalty,
            max_steps=max_steps,
            timeout_incomplete_penalty=premature_stop_penalty,
        )
