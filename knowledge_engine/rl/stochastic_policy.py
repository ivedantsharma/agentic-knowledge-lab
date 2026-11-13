"""EXP-116: gold-blind stochastic retrieval budgets and Monte Carlo rollouts.

Only RetrievalObservation is passed to a policy. Hidden supporting IDs
enter the environment for rewards and the evaluator for diagnostics.
No parameter updates or reinforcement learning occur in this module.
"""

from dataclasses import dataclass
from math import isfinite
from random import Random
from statistics import fmean, pstdev

from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisodeV2,
    RetrievalObservation,
    RetrievalRLAction,
)
from knowledge_engine.rl.trajectory_baselines import discounted_return

SEARCH_BUDGETS = (
    (RetrievalRLAction.SEARCH_K1, 1),
    (RetrievalRLAction.SEARCH_K2, 2),
    (RetrievalRLAction.SEARCH_K3, 3),
    (RetrievalRLAction.SEARCH_K5, 5),
)


def legal_actions(observation: RetrievalObservation) -> tuple[RetrievalRLAction, ...]:
    """Mask invalid/repeated search budgets without inspecting gold labels."""
    if observation.done:
        return ()
    return (
        RetrievalRLAction.STOP,
        *(action for action, budget in SEARCH_BUDGETS if budget > observation.requested_k),
    )


@dataclass(frozen=True)
class StochasticBudgetPolicy:
    """Epsilon-mixture over legal actions, preferring target when available.

    Once the target budget is no longer legal, the default greedy action is
    STOP; this is independent of supporting-document labels or rewards.
    """

    target: RetrievalRLAction
    epsilon: float

    def __post_init__(self) -> None:
        if not isinstance(self.target, RetrievalRLAction):
            raise ValueError("target must be a RetrievalRLAction")
        if not isfinite(self.epsilon) or not 0 <= self.epsilon <= 1:
            raise ValueError("epsilon must be finite and in [0, 1]")

    def probabilities(
        self, observation: RetrievalObservation
    ) -> dict[RetrievalRLAction, float]:
        actions = legal_actions(observation)
        if not actions:
            raise ValueError("cannot choose an action after episode termination")
        greedy = self.target if self.target in actions else RetrievalRLAction.STOP
        uniform_prob = self.epsilon / len(actions)
        return {
            action: uniform_prob + (1 - self.epsilon if action == greedy else 0.0)
            for action in actions
        }

    def sample_action(
        self, observation: RetrievalObservation, rng: Random
    ) -> RetrievalRLAction:
        probabilities = self.probabilities(observation)
        threshold = rng.random()
        cumulative = 0.0
        for action, probability in probabilities.items():
            cumulative += probability
            if threshold < cumulative:
                return action
        # Covers floating-point rounding if cumulative is slightly below 1.
        return next(reversed(probabilities))


@dataclass(frozen=True)
class SampledRollout:
    actions: tuple[RetrievalRLAction, ...]
    rewards: tuple[float, ...]
    final_observation: RetrievalObservation
    discounted_return: float

    @property
    def total_return(self) -> float:
        return sum(self.rewards)


def sample_rollout(
    *,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    policy: StochasticBudgetPolicy,
    rng: Random,
    gamma: float = 1.0,
    max_steps: int = 6,
) -> SampledRollout:
    """Roll out the policy. Gold IDs are never passed to sample_action."""
    discounted_return((), gamma=gamma)
    episode = RetrievalEpisodeV2(
        question=question,
        ranked_ids=ranked_ids,
        supporting_ids=supporting_ids,
        max_steps=max_steps,
    )
    actions: list[RetrievalRLAction] = []
    rewards: list[float] = []
    while not episode.observe().done:
        action = policy.sample_action(episode.observe(), rng)
        transition = episode.step(action)
        actions.append(action)
        rewards.append(transition.reward)
    return SampledRollout(
        actions=tuple(actions),
        rewards=tuple(rewards),
        final_observation=episode.observe(),
        discounted_return=discounted_return(rewards, gamma=gamma),
    )


@dataclass(frozen=True)
class MonteCarloSummary:
    episodes: int
    mean_return: float
    return_std: float
    mean_discounted_return: float
    mean_coverage: float
    completion_rate: float
    premature_stop_rate: float
    timeout_rate: float
    mean_documents: float
    mean_steps: float
    mean_conflicting_exposure: float
    unique_trajectories: int


def evaluate_policy(
    *,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    conflicting_ids: set[str],
    policy: StochasticBudgetPolicy,
    episodes: int,
    seed: int,
    gamma: float = 1.0,
    max_steps: int = 6,
) -> MonteCarloSummary:
    """Evaluator-only summary of actual on-policy sampled episodes."""
    if episodes <= 0:
        raise ValueError("episodes must be positive")
    if not conflicting_ids.issubset(set(ranked_ids)):
        raise ValueError("conflicting IDs must exist in ranking")
    rng = Random(seed)
    rollouts = [
        sample_rollout(
            question=question,
            ranked_ids=ranked_ids,
            supporting_ids=supporting_ids,
            policy=policy,
            rng=rng,
            gamma=gamma,
            max_steps=max_steps,
        )
        for _ in range(episodes)
    ]
    returns = [rollout.total_return for rollout in rollouts]
    coverage = [
        len(set(rollout.final_observation.retrieved_ids) & supporting_ids)
        / len(supporting_ids)
        for rollout in rollouts
    ]
    timeout = [rollout.actions[-1] != RetrievalRLAction.STOP for rollout in rollouts]
    premature = [
        rollout.actions[-1] == RetrievalRLAction.STOP and amount < 1.0
        for rollout, amount in zip(rollouts, coverage)
    ]
    return MonteCarloSummary(
        episodes=episodes,
        mean_return=fmean(returns),
        return_std=pstdev(returns),
        mean_discounted_return=fmean(rollout.discounted_return for rollout in rollouts),
        mean_coverage=fmean(coverage),
        completion_rate=sum(value == 1.0 for value in coverage) / episodes,
        premature_stop_rate=sum(premature) / episodes,
        timeout_rate=sum(timeout) / episodes,
        mean_documents=fmean(len(r.final_observation.retrieved_ids) for r in rollouts),
        mean_steps=fmean(len(r.actions) for r in rollouts),
        mean_conflicting_exposure=fmean(
            len(set(r.final_observation.retrieved_ids) & conflicting_ids)
            for r in rollouts
        ),
        unique_trajectories=len({r.actions for r in rollouts}),
    )
