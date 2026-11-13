"""EXP-114 deterministic counterfactual tests; no model inference required."""

from math import isclose

import pytest

from knowledge_engine.rl.retrieval_environment import RetrievalEpisodeV2, RetrievalRLAction
from scripts.run_phase12_reward_v2_trajectory_sweep import (
    RANKING,
    cases,
    increasing_search_prefixes,
    sweep_case,
)


@pytest.fixture(scope="module")
def case_results():
    return {
        case.name: sweep_case(case)
        for case in cases("Cirrus retry", frozenset({RANKING[1]}))
    }


def test_all_increasing_budget_prefixes_are_examined() -> None:
    sequences = increasing_search_prefixes()
    assert len(sequences) == 15
    assert len(set(sequences)) == 15
    assert (RetrievalRLAction.SEARCH_K1, RetrievalRLAction.SEARCH_K2) in sequences


def test_exp114_sweeps_sixty_termination_counterfactuals(case_results) -> None:
    assert len(case_results) == 4
    assert sum(map(len, case_results.values())) == 60


def test_incomplete_timeout_matches_stop_at_same_prefix(case_results) -> None:
    incomplete = [r for rows in case_results.values() for r in rows if r.v2_timeout.coverage < 1]
    assert len(incomplete) == 30
    for row in incomplete:
        assert isclose(row.v2_timeout.total_reward, row.v2_stop.total_reward, abs_tol=1e-9)
        assert isclose(
            row.v2_timeout.total_reward - row.v1_timeout.total_reward,
            -1.0,
            abs_tol=1e-9,
        )


def test_completed_prefixes_preserve_reward_and_stop_bonus(case_results) -> None:
    complete = [r for rows in case_results.values() for r in rows if r.v2_timeout.coverage == 1]
    assert len(complete) == 30
    for row in complete:
        assert isclose(row.v2_timeout.total_reward, row.v1_timeout.total_reward, abs_tol=1e-9)
        assert isclose(row.v2_stop.total_reward - row.v2_timeout.total_reward, 1, abs_tol=1e-9)


def test_partial_coverage_and_conflict_exposure_remain_diagnostics(case_results) -> None:
    two_support = case_results["synthetic_two_support"]
    assert any(row.v2_timeout.coverage == 0.5 for row in two_support)
    assert all(row.v2_timeout.conflicting_exposure_count == 1 for row in two_support)
    assert all(
        row.v2_timeout.conflicting_exposure_count == row.v1_timeout.conflicting_exposure_count
        for row in two_support
    )


def test_unreachable_support_is_detectable_not_misreported_as_success(case_results) -> None:
    unreachable = case_results["synthetic_out_of_budget"]
    assert all(row.v2_timeout.coverage == 0.0 for row in unreachable)
    assert all(
        row.v2_timeout.total_reward == pytest.approx(row.v2_stop.total_reward)
        for row in unreachable
    )


def test_same_or_smaller_budget_is_rejected() -> None:
    episode = RetrievalEpisodeV2("Find current evidence", list(RANKING), {RANKING[1]})
    episode.step(RetrievalRLAction.SEARCH_K2)
    with pytest.raises(ValueError, match="strictly increase"):
        episode.step(RetrievalRLAction.SEARCH_K2)
    with pytest.raises(ValueError, match="strictly increase"):
        episode.step(RetrievalRLAction.SEARCH_K1)


def test_saturated_larger_budget_has_no_positive_marginal_reward() -> None:
    episode = RetrievalEpisodeV2("Find evidence", ["first", "second"], {"second"})
    episode.step(RetrievalRLAction.SEARCH_K3)
    larger = episode.step(RetrievalRLAction.SEARCH_K5)
    assert larger.new_document_count == 0
    assert larger.new_support_count == 0
    assert larger.reward == pytest.approx(0.0)


def test_episode_rejects_steps_after_termination() -> None:
    episode = RetrievalEpisodeV2(
        "Find evidence", ["first", "second"], {"second"}, max_steps=1
    )
    episode.step(RetrievalRLAction.SEARCH_K1)
    with pytest.raises(ValueError, match="already ended"):
        episode.step(RetrievalRLAction.STOP)
