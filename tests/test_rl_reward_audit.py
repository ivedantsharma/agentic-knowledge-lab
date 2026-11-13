import pytest

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.rl.reward_audit import audit_trajectory


def test_conflicting_evidence_exposure_is_separate_from_reward() -> None:
    report, _ = audit_trajectory(
        question="Cirrus retry",
        ranked_ids=["pending", "current", "distractor"],
        supporting_ids={"current"},
        conflicting_ids={"pending"},
        actions=[
            RetrievalRLAction.SEARCH_K1,
            RetrievalRLAction.SEARCH_K2,
            RetrievalRLAction.STOP,
        ],
    )
    assert report.total_reward == pytest.approx(2.8)
    assert report.coverage == 1.0
    assert report.conflicting_exposure_count == 1
    assert report.stopped_explicitly


def test_timeout_has_no_explicit_stop_penalty_in_v1() -> None:
    report, _ = audit_trajectory(
        question="Evidence needed",
        ranked_ids=["distractor", "current"],
        supporting_ids={"current"},
        conflicting_ids=set(),
        actions=[RetrievalRLAction.SEARCH_K1],
        max_steps=1,
    )
    assert report.terminal_without_stop
    assert report.total_reward == pytest.approx(-0.1)
    assert report.coverage == 0.0


def test_premature_stop_penalty_differs_from_timeout() -> None:
    report, _ = audit_trajectory(
        question="Evidence needed",
        ranked_ids=["distractor", "current"],
        supporting_ids={"current"},
        conflicting_ids=set(),
        actions=[RetrievalRLAction.SEARCH_K1, RetrievalRLAction.STOP],
    )
    assert report.total_reward == pytest.approx(-1.1)
    assert not report.terminal_without_stop


def test_audit_rejects_unranked_conflicting_docs() -> None:
    with pytest.raises(ValueError):
        audit_trajectory(
            question="Evidence needed",
            ranked_ids=["current"],
            supporting_ids={"current"},
            conflicting_ids={"missing"},
            actions=[RetrievalRLAction.SEARCH_K1],
        )
