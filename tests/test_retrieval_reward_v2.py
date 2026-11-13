import pytest

from knowledge_engine.rl.reward_audit import audit_trajectory
from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisode,
    RetrievalEpisodeV2,
    RetrievalRLAction,
)


def _episode(cls, max_steps: int):
    return cls(
        "Find current evidence",
        ["pending", "current", "other"],
        {"current"},
        max_steps=max_steps,
    )


def test_v2_forced_incomplete_timeout_matches_early_stop_return() -> None:
    timeout = _episode(RetrievalEpisodeV2, max_steps=1)
    timeout_reward = timeout.step(RetrievalRLAction.SEARCH_K1).reward

    early = _episode(RetrievalEpisodeV2, max_steps=6)
    first = early.step(RetrievalRLAction.SEARCH_K1).reward
    stop = early.step(RetrievalRLAction.STOP).reward

    assert timeout_reward == pytest.approx(-1.1)
    assert timeout_reward == pytest.approx(first + stop)


def test_v1_timeout_behavior_is_preserved() -> None:
    episode = _episode(RetrievalEpisode, max_steps=1)
    assert episode.step(RetrievalRLAction.SEARCH_K1).reward == pytest.approx(-0.1)


def test_v2_complete_timeout_not_penalized_as_incomplete() -> None:
    episode = _episode(RetrievalEpisodeV2, max_steps=1)
    step = episode.step(RetrievalRLAction.SEARCH_K2)
    assert step.reward == pytest.approx(1.8)
    assert step.next_observation.done


def test_v2_gold_labels_stay_out_of_observation() -> None:
    episode = _episode(RetrievalEpisodeV2, max_steps=6)
    assert not hasattr(episode.observe(), "supporting_ids")
    assert episode.observe().retrieved_ids == ()


def test_v2_reward_audit_preserves_conflicting_exposure() -> None:
    report, _transitions = audit_trajectory(
        question="Current policy?",
        ranked_ids=["pending", "current", "other"],
        supporting_ids={"current"},
        conflicting_ids={"pending"},
        actions=[
            RetrievalRLAction.SEARCH_K1,
            RetrievalRLAction.SEARCH_K2,
            RetrievalRLAction.STOP,
        ],
        reward_version="v2",
    )
    assert report.total_reward == pytest.approx(2.8)
    assert report.conflicting_exposure_count == 1


def test_v2_and_v1_completed_stop_equal() -> None:
    values = []
    for cls in (RetrievalEpisode, RetrievalEpisodeV2):
        episode = _episode(cls, max_steps=6)
        values.append(
            episode.step(RetrievalRLAction.SEARCH_K2).reward
            + episode.step(RetrievalRLAction.STOP).reward
        )
    assert values[0] == pytest.approx(values[1])
