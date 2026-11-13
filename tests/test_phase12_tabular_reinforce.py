"""EXP-117 tests: gradient correctness, reproducible updates, gold separation."""

from math import isclose, log
from random import Random

import pytest

from knowledge_engine.rl.reinforce import (
    TabularSoftmaxPolicy,
    evaluate_learned_policy,
    log_probability_gradient,
    returns_to_go,
    rollout,
    state_key,
    train_reinforce,
)
from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisodeV2,
    RetrievalRLAction,
)

A = RetrievalRLAction
RANKING = ["pending", "current", "other", "late", "fifth"]


def environment(support: set[str] | None = None) -> dict:
    return {
        "question": "What is current?",
        "ranked_ids": RANKING.copy(),
        "supporting_ids": {"current"} if support is None else support,
    }


def initial_observation():
    return RetrievalEpisodeV2(**environment()).observe()


def test_uniform_policy_probability_and_legal_mask() -> None:
    model = TabularSoftmaxPolicy()
    obs = initial_observation()
    initial = model.probabilities(obs)
    assert len(initial) == 5
    assert all(prob == pytest.approx(0.2) for prob in initial.values())
    assert sum(initial.values()) == pytest.approx(1.0)
    after_k2 = RetrievalEpisodeV2(**environment())
    after_k2.step(A.SEARCH_K2)
    masked = model.probabilities(after_k2.observe())
    assert set(masked) == {A.STOP, A.SEARCH_K3, A.SEARCH_K5}


def test_terminal_observation_cannot_be_sampled() -> None:
    episode = RetrievalEpisodeV2(**environment())
    episode.step(A.STOP)
    with pytest.raises(ValueError, match="terminal"):
        TabularSoftmaxPolicy().probabilities(episode.observe())


def test_visible_state_key_has_no_gold_features() -> None:
    first = RetrievalEpisodeV2(**environment({"current"})).observe()
    second = RetrievalEpisodeV2(**environment({"late"})).observe()
    assert state_key(first) == state_key(second) == (0, 0)
    assert not hasattr(first, "supporting_ids")


def test_softmax_gradient_is_zero_sum() -> None:
    model = TabularSoftmaxPolicy()
    probs = model.probabilities(initial_observation())
    gradient = log_probability_gradient(probs, A.SEARCH_K2)
    assert sum(gradient.values()) == pytest.approx(0)
    assert gradient[A.SEARCH_K2] == pytest.approx(0.8)
    assert gradient[A.STOP] == pytest.approx(-0.2)
    with pytest.raises(ValueError, match="legal"):
        log_probability_gradient({A.STOP: 1.0}, A.SEARCH_K2)


def test_log_probability_gradient_matches_finite_difference() -> None:
    model = TabularSoftmaxPolicy()
    observation = initial_observation()
    probabilities = model.probabilities(observation)
    analytic = log_probability_gradient(probabilities, A.SEARCH_K2)
    epsilon = 1e-6
    for action in probabilities:
        plus = model.clone()
        minus = model.clone()
        plus.logits[(0, 0)][action] += epsilon
        minus.logits[(0, 0)][action] -= epsilon
        log_plus = log(plus.probabilities(observation)[A.SEARCH_K2])
        log_minus = log(minus.probabilities(observation)[A.SEARCH_K2])
        numeric = (log_plus - log_minus) / (2 * epsilon)
        assert analytic[action] == pytest.approx(numeric, abs=1e-8)


def test_returns_to_go_and_discount() -> None:
    values = returns_to_go((-0.1, 1.9, 1.0), gamma=0.9)
    assert values == pytest.approx((2.42, 2.8, 1.0))
    assert returns_to_go((), gamma=1.0) == ()
    with pytest.raises(ValueError, match="gamma"):
        returns_to_go((1.0,), gamma=1.1)


def test_policy_clone_is_independent() -> None:
    model = TabularSoftmaxPolicy()
    model.probabilities(initial_observation())
    clone = model.clone()
    clone.logits[(0, 0)][A.SEARCH_K2] = 8.0
    assert model.logits[(0, 0)][A.SEARCH_K2] == 0.0
    assert clone.probabilities(initial_observation())[A.SEARCH_K2] > 0.99


def test_seeded_rollout_reproducible() -> None:
    model = TabularSoftmaxPolicy()
    a = rollout(policy=model, **environment(), rng=Random(117))
    b = rollout(policy=model, **environment(), rng=Random(117))
    assert a == b
    assert len(a.actions) >= 1
    assert a.final_observation.done


def test_identical_visible_state_hidden_gold_changes_reward_not_actions() -> None:
    model = TabularSoftmaxPolicy()
    model.probabilities(initial_observation())
    model.logits[(0, 0)][A.SEARCH_K2] = 100.0
    first = rollout(policy=model, **environment({"current"}), rng=Random(117))
    second = rollout(policy=model, **environment({"late"}), rng=Random(117))
    assert first.actions == second.actions
    assert first.final_observation == second.final_observation
    assert first.rewards != second.rewards


def test_training_changes_action_probabilities_on_grounded_like_case() -> None:
    model = TabularSoftmaxPolicy()
    before = evaluate_learned_policy(
        policy=model, **environment(), conflicting_ids={"pending"}, episodes=400, seed=4000
    )
    history = train_reinforce(policy=model, **environment(), episodes=600, seed=0)
    after = evaluate_learned_policy(
        policy=model, **environment(), conflicting_ids={"pending"}, episodes=400, seed=4000
    )
    assert history.episodes == 600
    assert history.states_visited > 0
    assert after.mean_discounted_return > before.mean_discounted_return + 0.3
    assert after.completion_rate > before.completion_rate
    assert model.probabilities(initial_observation())[A.SEARCH_K2] > 0.5


def test_zero_learning_rate_keeps_policy_fixed() -> None:
    model = TabularSoftmaxPolicy()
    before = evaluate_learned_policy(
        policy=model, **environment(), conflicting_ids=set(), episodes=100, seed=4000
    )
    summary = train_reinforce(
        policy=model, **environment(), episodes=100, seed=0, learning_rate=0.0
    )
    after = evaluate_learned_policy(
        policy=model, **environment(), conflicting_ids=set(), episodes=100, seed=4000
    )
    assert summary.episodes == 100
    assert after == before
    for row in model.logits.values():
        assert all(isclose(value, 0.0, abs_tol=1e-10) for value in row.values())


def test_training_same_seed_is_reproducible() -> None:
    first = TabularSoftmaxPolicy()
    second = TabularSoftmaxPolicy()
    a = train_reinforce(policy=first, **environment(), episodes=120, seed=7)
    b = train_reinforce(policy=second, **environment(), episodes=120, seed=7)
    assert a == b
    assert first.logits == second.logits


@pytest.mark.parametrize("bad", [-0.1, float("inf"), float("nan")])
def test_invalid_learning_rate(bad: float) -> None:
    with pytest.raises(ValueError, match="learning_rate"):
        train_reinforce(
            policy=TabularSoftmaxPolicy(),
            **environment(),
            episodes=1,
            seed=0,
            learning_rate=bad,
        )


@pytest.mark.parametrize("bad", [-0.1, 1.1, float("nan")])
def test_invalid_baseline_rate(bad: float) -> None:
    with pytest.raises(ValueError, match="baseline_rate"):
        train_reinforce(
            policy=TabularSoftmaxPolicy(),
            **environment(),
            episodes=1,
            seed=0,
            baseline_rate=bad,
        )


def test_training_rejects_zero_episodes() -> None:
    with pytest.raises(ValueError, match="episodes"):
        train_reinforce(
            policy=TabularSoftmaxPolicy(), **environment(), episodes=0, seed=0
        )


def test_evaluation_rejects_invalid_arguments() -> None:
    with pytest.raises(ValueError, match="episodes"):
        evaluate_learned_policy(
            policy=TabularSoftmaxPolicy(),
            **environment(),
            conflicting_ids=set(),
            episodes=0,
            seed=1,
        )
    with pytest.raises(ValueError, match="conflicting IDs"):
        evaluate_learned_policy(
            policy=TabularSoftmaxPolicy(),
            **environment(),
            conflicting_ids={"unranked"},
            episodes=1,
            seed=1,
        )


def test_policy_logit_extremes_do_not_overflow() -> None:
    model = TabularSoftmaxPolicy()
    model.probabilities(initial_observation())
    model.logits[(0, 0)][A.SEARCH_K2] = 1000.0
    probabilities = model.probabilities(initial_observation())
    assert probabilities[A.SEARCH_K2] == pytest.approx(1.0)
    assert sum(probabilities.values()) == pytest.approx(1.0)


def test_forced_timeout_under_short_horizon() -> None:
    model = TabularSoftmaxPolicy()
    initial = initial_observation()
    model.probabilities(initial)
    model.logits[(0, 0)][A.SEARCH_K1] = 100.0
    episode = RetrievalEpisodeV2(**environment())
    episode.step(A.SEARCH_K1)
    model.probabilities(episode.observe())
    model.logits[(1, 1)][A.SEARCH_K2] = 100.0
    trace = rollout(policy=model, **environment(), rng=Random(1), max_steps=2)
    assert trace.actions == (A.SEARCH_K1, A.SEARCH_K2)
    assert trace.final_observation.done
    assert trace.rewards == pytest.approx((-0.1, 1.9))
