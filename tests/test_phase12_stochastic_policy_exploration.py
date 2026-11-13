"""EXP-116: stochastic policies must be legal, reproducible and gold-blind."""

from random import Random

import pytest

from knowledge_engine.rl.retrieval_environment import RetrievalObservation
from knowledge_engine.rl.retrieval_environment import RetrievalRLAction as A
from knowledge_engine.rl.stochastic_policy import (
    StochasticBudgetPolicy,
    evaluate_policy,
    legal_actions,
    sample_rollout,
)


RANKING = ["pending", "current", "distractor", "other", "late"]


def observation(k: int = 0, *, done: bool = False) -> RetrievalObservation:
    return RetrievalObservation(
        question="What is current?",
        retrieved_ids=tuple(RANKING[:k]),
        requested_k=k,
        steps_taken=int(k > 0),
        done=done,
    )


def kwargs(supporting: set[str] | None = None) -> dict:
    return {
        "question": "What is current?",
        "ranked_ids": RANKING.copy(),
        "supporting_ids": {"current"} if supporting is None else supporting,
    }


def test_action_mask_excludes_repeated_and_smaller_budgets() -> None:
    assert legal_actions(observation()) == (
        A.STOP, A.SEARCH_K1, A.SEARCH_K2, A.SEARCH_K3, A.SEARCH_K5
    )
    assert legal_actions(observation(2)) == (A.STOP, A.SEARCH_K3, A.SEARCH_K5)
    assert legal_actions(observation(5)) == (A.STOP,)
    assert legal_actions(observation(5, done=True)) == ()


def test_epsilon_zero_is_deterministic_target_then_stop() -> None:
    policy = StochasticBudgetPolicy(A.SEARCH_K2, epsilon=0)
    assert policy.probabilities(observation())[A.SEARCH_K2] == 1.0
    assert policy.probabilities(observation(2))[A.STOP] == 1.0
    assert policy.probabilities(observation(5)) == {A.STOP: 1.0}


def test_epsilon_one_is_uniform_over_only_legal_actions() -> None:
    policy = StochasticBudgetPolicy(A.SEARCH_K2, epsilon=1)
    initial = policy.probabilities(observation())
    assert len(initial) == 5
    assert all(prob == pytest.approx(0.2) for prob in initial.values())
    after_k2 = policy.probabilities(observation(2))
    assert len(after_k2) == 3
    assert all(prob == pytest.approx(1 / 3) for prob in after_k2.values())


def test_epsilon_mixture_probability_mass() -> None:
    policy = StochasticBudgetPolicy(A.SEARCH_K2, epsilon=0.2)
    for k in (0, 1, 2, 3, 5):
        distribution = policy.probabilities(observation(k))
        assert sum(distribution.values()) == pytest.approx(1.0)
        assert all(prob >= 0 for prob in distribution.values())
        assert all(action in legal_actions(observation(k)) for action in distribution)
    assert policy.probabilities(observation())[A.SEARCH_K2] == pytest.approx(0.84)


@pytest.mark.parametrize("epsilon", [-0.1, 1.1, float("nan"), float("inf")])
def test_invalid_epsilon_rejected(epsilon: float) -> None:
    with pytest.raises(ValueError, match="epsilon"):
        StochasticBudgetPolicy(A.SEARCH_K2, epsilon=epsilon)


def test_invalid_target_rejected() -> None:
    with pytest.raises(TypeError, match="target"):
        StochasticBudgetPolicy("SEARCH_K2", epsilon=0.2)


def test_cannot_sample_after_done() -> None:
    with pytest.raises(ValueError, match="after episode termination"):
        StochasticBudgetPolicy(A.SEARCH_K2, epsilon=0.2).sample_action(
            observation(done=True), Random(1)
        )


def test_fixed_seed_produces_identical_trajectory() -> None:
    policy = StochasticBudgetPolicy(A.SEARCH_K2, epsilon=0.4)
    x = sample_rollout(**kwargs(), policy=policy, rng=Random(123))
    y = sample_rollout(**kwargs(), policy=policy, rng=Random(123))
    assert x == y


def test_hidden_gold_change_does_not_change_actions() -> None:
    """Identical visible observations + RNG => identical policy decisions."""
    policy = StochasticBudgetPolicy(A.SEARCH_K2, epsilon=0.0)
    a = sample_rollout(**kwargs({"current"}), policy=policy, rng=Random(116))
    b = sample_rollout(**kwargs({"late"}), policy=policy, rng=Random(116))
    assert a.actions == b.actions == (A.SEARCH_K2, A.STOP)
    assert a.final_observation == b.final_observation
    assert a.rewards != b.rewards
    assert not hasattr(a.final_observation, "supporting_ids")


def test_zero_exploration_matches_existing_fixed_k2_baseline() -> None:
    report = evaluate_policy(
        **kwargs(),
        conflicting_ids={"pending"},
        policy=StochasticBudgetPolicy(A.SEARCH_K2, epsilon=0),
        episodes=20,
        seed=1,
    )
    assert report.mean_return == pytest.approx(2.8)
    assert report.return_std == pytest.approx(0.0)
    assert report.completion_rate == pytest.approx(1.0)
    assert report.mean_coverage == pytest.approx(1.0)
    assert report.mean_documents == pytest.approx(2.0)
    assert report.mean_conflicting_exposure == pytest.approx(1.0)
    assert report.unique_trajectories == 1
    assert report.timeout_rate == 0.0


def test_uniform_exploration_samples_multiple_paths_without_default_timeout() -> None:
    report = evaluate_policy(
        **kwargs(),
        conflicting_ids={"pending"},
        policy=StochasticBudgetPolicy(A.STOP, epsilon=1),
        episodes=300,
        seed=116,
        gamma=0.9,
        max_steps=6,
    )
    assert report.return_std > 0
    assert report.unique_trajectories >= 5
    assert 0 < report.completion_rate < 1
    assert report.timeout_rate == 0.0
    assert 0 < report.mean_coverage < 1


def test_tight_horizon_can_timeout_where_default_horizon_cannot() -> None:
    inputs = {
        **kwargs(),
        "conflicting_ids": {"pending"},
        "policy": StochasticBudgetPolicy(A.STOP, epsilon=1),
        "episodes": 400,
        "seed": 116,
    }
    short = evaluate_policy(**inputs, max_steps=2)
    normal = evaluate_policy(**inputs, max_steps=6)
    assert short.timeout_rate > 0
    assert normal.timeout_rate == 0.0


def test_complete_and_incomplete_forced_timeouts_differ() -> None:
    fixed_k2 = StochasticBudgetPolicy(A.SEARCH_K2, epsilon=0)
    complete = sample_rollout(**kwargs(), policy=fixed_k2, rng=Random(1), max_steps=1)
    incomplete = sample_rollout(
        **kwargs({"late"}), policy=fixed_k2, rng=Random(1), max_steps=1
    )
    assert complete.actions == incomplete.actions == (A.SEARCH_K2,)
    assert complete.total_return == pytest.approx(1.8)
    assert incomplete.total_return == pytest.approx(-1.2)


def test_seeded_monte_carlo_summary_is_reproducible() -> None:
    settings = {
        **kwargs(),
        "conflicting_ids": {"pending"},
        "policy": StochasticBudgetPolicy(A.SEARCH_K5, epsilon=0.2),
        "episodes": 150,
        "seed": 116,
        "gamma": 0.9,
        "max_steps": 2,
    }
    assert evaluate_policy(**settings) == evaluate_policy(**settings)


def test_unreachable_evidence_has_zero_completion() -> None:
    inputs = kwargs({"sixth"})
    inputs["ranked_ids"].append("sixth")
    report = evaluate_policy(
        **inputs,
        conflicting_ids={"pending"},
        policy=StochasticBudgetPolicy(A.SEARCH_K5, epsilon=0.2),
        episodes=100,
        seed=116,
    )
    assert report.completion_rate == 0.0
    assert report.mean_coverage == 0.0


def test_invalid_episode_count_and_conflict_ids_rejected() -> None:
    inputs = kwargs()
    policy = StochasticBudgetPolicy(A.STOP, epsilon=1)
    with pytest.raises(ValueError, match="episodes"):
        evaluate_policy(
            **inputs, conflicting_ids=set(), policy=policy, episodes=0, seed=1
        )
    with pytest.raises(ValueError, match="conflicting IDs"):
        evaluate_policy(
            **inputs, conflicting_ids={"not-ranked"}, policy=policy, episodes=1, seed=1
        )
