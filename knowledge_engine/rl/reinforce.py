"""EXP-117: minimal on-policy tabular REINFORCE for retrieval control.

Training updates policy logits using sampled trajectories and Reward v2.
Gold supporting IDs are passed ONLY to the environment/evaluator; the
policy is conditioned on (requested_k, steps_taken), not gold labels.
This deliberately tests learning mechanics, NOT cross-task generalization.
"""

from dataclasses import dataclass
from math import exp, isfinite
from random import Random
from statistics import fmean, pstdev

from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisodeV2,
    RetrievalObservation,
    RetrievalRLAction,
)
from knowledge_engine.rl.stochastic_policy import legal_actions
from knowledge_engine.rl.trajectory_baselines import discounted_return

StateKey = tuple[int, int]


def state_key(observation: RetrievalObservation) -> StateKey:
    """Visible state only; no supporting IDs or reward are policy features."""
    return (observation.requested_k, observation.steps_taken)


def sample_distribution(
    probabilities: dict[RetrievalRLAction, float], rng: Random
) -> RetrievalRLAction:
    threshold = rng.random()
    accumulated = 0.0
    for action, probability in probabilities.items():
        accumulated += probability
        if threshold < accumulated:
            return action
    return next(reversed(probabilities))


def log_probability_gradient(
    probabilities: dict[RetrievalRLAction, float], selected: RetrievalRLAction
) -> dict[RetrievalRLAction, float]:
    """Derivative of log softmax(selected) with respect to each legal logit."""
    if selected not in probabilities:
        raise ValueError("selected action must be legal")
    return {
        action: float(action == selected) - probability
        for action, probability in probabilities.items()
    }


def returns_to_go(rewards: tuple[float, ...], *, gamma: float) -> tuple[float, ...]:
    """G_t = r_t + gamma*G_(t+1); used for per-action credit assignment."""
    discounted_return((), gamma=gamma)
    values = [0.0] * len(rewards)
    running = 0.0
    for index in range(len(rewards) - 1, -1, -1):
        running = rewards[index] + gamma * running
        values[index] = running
    return tuple(values)


class TabularSoftmaxPolicy:
    """A small, inspectable state-to-action probability table.

    This is NOT a language model; question text and document contents are
    deliberately not embedded. It cannot personalize choices by task family.
    """

    def __init__(self) -> None:
        self.logits: dict[StateKey, dict[RetrievalRLAction, float]] = {}

    def probabilities(
        self, observation: RetrievalObservation
    ) -> dict[RetrievalRLAction, float]:
        actions = legal_actions(observation)
        if not actions:
            raise ValueError("cannot sample a terminal observation")
        key = state_key(observation)
        row = self.logits.setdefault(key, {action: 0.0 for action in actions})
        if set(row) != set(actions):
            raise ValueError("inconsistent action mask for state")
        highest = max(row.values())
        weights = {action: exp(row[action] - highest) for action in actions}
        denominator = sum(weights.values())
        return {action: weight / denominator for action, weight in weights.items()}

    def sample_action(
        self, observation: RetrievalObservation, rng: Random
    ) -> RetrievalRLAction:
        return sample_distribution(self.probabilities(observation), rng)

    def clone(self) -> "TabularSoftmaxPolicy":
        result = TabularSoftmaxPolicy()
        result.logits = {key: row.copy() for key, row in self.logits.items()}
        return result


@dataclass(frozen=True)
class PolicyGradientStep:
    observation: RetrievalObservation
    action: RetrievalRLAction
    probabilities: dict[RetrievalRLAction, float]
    reward: float


@dataclass(frozen=True)
class PolicyGradientRollout:
    steps: tuple[PolicyGradientStep, ...]
    final_observation: RetrievalObservation

    @property
    def actions(self) -> tuple[RetrievalRLAction, ...]:
        return tuple(step.action for step in self.steps)

    @property
    def rewards(self) -> tuple[float, ...]:
        return tuple(step.reward for step in self.steps)


def rollout(
    *,
    policy: TabularSoftmaxPolicy,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    rng: Random,
    max_steps: int = 6,
) -> PolicyGradientRollout:
    """Sample an entire trajectory with fixed policy parameters."""
    episode = RetrievalEpisodeV2(
        question=question,
        ranked_ids=ranked_ids,
        supporting_ids=supporting_ids,
        max_steps=max_steps,
    )
    transitions: list[PolicyGradientStep] = []
    while not episode.observe().done:
        observation = episode.observe()
        probabilities = policy.probabilities(observation)
        action = sample_distribution(probabilities, rng)
        transition = episode.step(action)
        transitions.append(
            PolicyGradientStep(observation, action, probabilities, transition.reward)
        )
    return PolicyGradientRollout(tuple(transitions), episode.observe())


@dataclass(frozen=True)
class TrainingSummary:
    episodes: int
    early_mean_discounted_return: float
    late_mean_discounted_return: float
    states_visited: int


def train_reinforce(
    *,
    policy: TabularSoftmaxPolicy,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    episodes: int,
    seed: int,
    learning_rate: float = 0.08,
    baseline_rate: float = 0.05,
    gamma: float = 0.9,
    max_steps: int = 6,
) -> TrainingSummary:
    """REINFORCE with a state-dependent EMA baseline and on-policy samples.

    To optimize expected discounted G_0, each step's gradient carries
    gamma**t * (G_t - baseline_t). The baseline uses earlier rollouts only,
    and is updated AFTER each step gradient, avoiding current-reward leakage
    into its own baseline estimate.
    """
    if episodes < 1:
        raise ValueError("episodes must be positive")
    if not isfinite(learning_rate) or learning_rate < 0:
        raise ValueError("learning_rate must be finite and nonnegative")
    if not isfinite(baseline_rate) or not 0 <= baseline_rate <= 1:
        raise ValueError("baseline_rate must be in [0, 1]")
    discounted_return((), gamma=gamma)
    rng = Random(seed)
    baseline: dict[StateKey, float] = {}
    results: list[float] = []
    for _ in range(episodes):
        trajectory = rollout(
            policy=policy,
            question=question,
            ranked_ids=ranked_ids,
            supporting_ids=supporting_ids,
            rng=rng,
            max_steps=max_steps,
        )
        rewards = trajectory.rewards
        results.append(discounted_return(rewards, gamma=gamma))
        returns = returns_to_go(rewards, gamma=gamma)
        for timestep, (step, target) in enumerate(zip(trajectory.steps, returns)):
            key = state_key(step.observation)
            prior_baseline = baseline.get(key, 0.0)
            advantage = target - prior_baseline
            scale = learning_rate * (gamma**timestep) * advantage
            gradient = log_probability_gradient(step.probabilities, step.action)
            for action, derivative in gradient.items():
                policy.logits[key][action] += scale * derivative
            baseline[key] = prior_baseline + baseline_rate * advantage

    window = min(100, episodes)
    return TrainingSummary(
        episodes=episodes,
        early_mean_discounted_return=fmean(results[:window]),
        late_mean_discounted_return=fmean(results[-window:]),
        states_visited=len(policy.logits),
    )


@dataclass(frozen=True)
class LearnedPolicyEvaluation:
    episodes: int
    mean_discounted_return: float
    return_std: float
    mean_coverage: float
    completion_rate: float
    premature_stop_rate: float
    timeout_rate: float
    mean_documents: float
    mean_conflicting_exposure: float
    unique_trajectories: int


def evaluate_learned_policy(
    *,
    policy: TabularSoftmaxPolicy,
    question: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    conflicting_ids: set[str],
    episodes: int,
    seed: int,
    gamma: float = 0.9,
    max_steps: int = 6,
) -> LearnedPolicyEvaluation:
    """Independent on-policy evaluation; no updates during evaluation."""
    if episodes < 1:
        raise ValueError("episodes must be positive")
    if not conflicting_ids.issubset(set(ranked_ids)):
        raise ValueError("conflicting IDs must exist in ranking")
    discounted_return((), gamma=gamma)
    rng = Random(seed)
    trajectories = [
        rollout(
            policy=policy,
            question=question,
            ranked_ids=ranked_ids,
            supporting_ids=supporting_ids,
            rng=rng,
            max_steps=max_steps,
        )
        for _ in range(episodes)
    ]
    scores = [discounted_return(t.rewards, gamma=gamma) for t in trajectories]
    coverage = [
        len(set(t.final_observation.retrieved_ids) & supporting_ids) / len(supporting_ids)
        for t in trajectories
    ]
    prematurely_stopped = [
        t.actions[-1] == RetrievalRLAction.STOP and amount < 1.0
        for t, amount in zip(trajectories, coverage)
    ]
    timeouts = [t.actions[-1] != RetrievalRLAction.STOP for t in trajectories]
    return LearnedPolicyEvaluation(
        episodes=episodes,
        mean_discounted_return=fmean(scores),
        return_std=pstdev(scores),
        mean_coverage=fmean(coverage),
        completion_rate=sum(value == 1.0 for value in coverage) / episodes,
        premature_stop_rate=sum(prematurely_stopped) / episodes,
        timeout_rate=sum(timeouts) / episodes,
        mean_documents=fmean(len(t.final_observation.retrieved_ids) for t in trajectories),
        mean_conflicting_exposure=fmean(
            len(set(t.final_observation.retrieved_ids) & conflicting_ids)
            for t in trajectories
        ),
        unique_trajectories=len({t.actions for t in trajectories}),
    )
