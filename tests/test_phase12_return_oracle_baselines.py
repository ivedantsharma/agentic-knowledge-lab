"""EXP-115 tests: no model inference, hidden-label oracle only as upper bound."""

from math import isclose

import pytest

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction as A
from knowledge_engine.rl.trajectory_baselines import (
    discounted_return,
    fixed_policy_actions,
    legal_terminated_trajectories,
    oracle_trajectory,
    score_trajectory,
)

RANKING = ["pending", "current", "distractor", "other", "late"]


def _case(supporting_ids: set[str] | None = None) -> dict:
    return {
        "question": "What is current?",
        "ranked_ids": RANKING.copy(),
        "supporting_ids": supporting_ids or {"current"},
        "conflicting_ids": {"pending"},
    }


def test_discounted_return_and_gamma_one() -> None:
    assert discounted_return([-0.1, 1.9, 1.0]) == pytest.approx(2.8)
    assert discounted_return([-0.1, 1.9, 1.0], gamma=0.9) == pytest.approx(2.42)
    assert discounted_return([-0.1, 1.9, 1.0], gamma=0) == pytest.approx(-0.1)


@pytest.mark.parametrize("gamma", [-0.1, 1.1, float("nan"), float("inf")])
def test_gamma_outside_range_is_invalid(gamma: float) -> None:
    with pytest.raises(ValueError, match="gamma"):
        discounted_return([1.0], gamma=gamma)


def test_terminal_enumeration_covers_every_increasing_prefix() -> None:
    paths = legal_terminated_trajectories(max_steps=6)
    assert len(paths) == 16  # STOP_NOW + all 15 legal search subsets then STOP
    assert len(set(paths)) == 16
    assert all(path[-1] == A.STOP for path in paths)
    assert (A.SEARCH_K2, A.STOP) in paths


def test_short_horizon_explicitly_includes_timeout_paths() -> None:
    paths = legal_terminated_trajectories(max_steps=1)
    assert len(paths) == 5
    assert (A.STOP,) in paths
    assert (A.SEARCH_K1,) in paths
    assert (A.SEARCH_K5,) in paths
    assert (A.SEARCH_K1, A.STOP) not in paths


def test_terminal_enumeration_rejects_invalid_horizon() -> None:
    with pytest.raises(ValueError, match="positive"):
        legal_terminated_trajectories(max_steps=0)


def test_trajectory_scoring_requires_terminal_action() -> None:
    with pytest.raises(ValueError, match="must terminate"):
        score_trajectory(**_case(), actions=(A.SEARCH_K2,), max_steps=6)


def test_grounded_like_cirrus_oracle_finds_minimal_support_budget() -> None:
    oracle = oracle_trajectory(**_case())
    assert oracle.actions == (A.SEARCH_K2, A.STOP)
    assert oracle.report.total_reward == pytest.approx(2.8)
    assert oracle.report.coverage == 1.0
    assert oracle.report.retrieval_cost_count == 2
    assert oracle.report.conflicting_exposure_count == 1


def test_fixed_policy_has_no_access_to_gold_labels() -> None:
    policies = fixed_policy_actions()
    assert len(policies) == 6
    assert policies["STOP_NOW"] == (A.STOP,)
    assert policies["FIXED_K5"] == (A.SEARCH_K5, A.STOP)
    assert policies["ESCALATE"][-1] == A.STOP


def test_oracle_outperforms_fixed_k5_on_cirrus_ranking() -> None:
    oracle = oracle_trajectory(**_case())
    fixed = score_trajectory(**_case(), actions=fixed_policy_actions()["FIXED_K5"])
    assert oracle.report.total_reward == pytest.approx(2.8)
    assert fixed.report.total_reward == pytest.approx(2.5)
    assert oracle.report.coverage == fixed.report.coverage == 1.0


def test_direct_and_staged_search_tie_at_gamma_one_but_not_point_nine() -> None:
    direct = (A.SEARCH_K2, A.STOP)
    staged = (A.SEARCH_K1, A.SEARCH_K2, A.STOP)
    for gamma in (1.0, 0.9):
        a = score_trajectory(**_case(), actions=direct, gamma=gamma)
        b = score_trajectory(**_case(), actions=staged, gamma=gamma)
        if gamma == 1.0:
            assert isclose(a.discounted_return, b.discounted_return, abs_tol=1e-9)
        else:
            assert a.discounted_return > b.discounted_return
            assert a.discounted_return == pytest.approx(2.7)
            assert b.discounted_return == pytest.approx(2.42)


def test_gold_oracle_prefers_stop_when_support_is_out_of_budget() -> None:
    kwargs = _case()
    kwargs["ranked_ids"].append("sixth")
    kwargs["supporting_ids"] = {"sixth"}
    oracle = oracle_trajectory(**kwargs)
    assert oracle.actions == (A.STOP,)
    assert oracle.report.total_reward == pytest.approx(-1.0)
    assert oracle.report.coverage == 0.0


def test_two_support_oracle_chooses_k5() -> None:
    oracle = oracle_trajectory(**_case({"current", "other"}))
    assert oracle.actions == (A.SEARCH_K5, A.STOP)
    assert oracle.report.total_reward == pytest.approx(4.5)
    assert oracle.report.coverage == 1.0


def test_max_steps_one_oracle_can_finish_by_complete_timeout() -> None:
    oracle = oracle_trajectory(**_case(), max_steps=1)
    assert oracle.actions == (A.SEARCH_K2,)
    assert oracle.report.terminal_without_stop
    assert oracle.report.total_reward == pytest.approx(1.8)


def test_oracle_upper_bounds_each_fixed_policy() -> None:
    oracle = oracle_trajectory(**_case(), gamma=0.9)
    for actions in fixed_policy_actions().values():
        policy = score_trajectory(**_case(), actions=actions, gamma=0.9)
        assert oracle.discounted_return + 1e-9 >= policy.discounted_return
