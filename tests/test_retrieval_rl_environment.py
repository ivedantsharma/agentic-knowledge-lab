import pytest

from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisode,
    RetrievalRLAction,
    total_return,
)


def make_episode() -> RetrievalEpisode:
    return RetrievalEpisode(
        "Find the evidence",
        ["distractor", "support", "other"],
        {"support"},
    )


def test_expanding_budget_rewards_new_evidence_only_once() -> None:
    episode = make_episode()
    first = episode.step(RetrievalRLAction.SEARCH_K1)
    second = episode.step(RetrievalRLAction.SEARCH_K2)
    stopped = episode.step(RetrievalRLAction.STOP)

    assert first.reward == pytest.approx(-0.1)
    assert second.reward == pytest.approx(1.9)
    assert stopped.reward == pytest.approx(1.0)
    assert total_return([first, second, stopped]) == pytest.approx(2.8)
    assert second.new_support_count == 1


def test_premature_stop_penalized() -> None:
    episode = make_episode()
    episode.step(RetrievalRLAction.SEARCH_K1)
    stopped = episode.step(RetrievalRLAction.STOP)
    assert stopped.reward == -1.0
    assert stopped.next_observation.done


def test_observation_does_not_expose_gold() -> None:
    episode = make_episode()
    assert not hasattr(episode.observe(), "supporting_ids")
    assert episode.observe().retrieved_ids == ()


def test_repeated_or_smaller_budget_is_invalid() -> None:
    episode = make_episode()
    episode.step(RetrievalRLAction.SEARCH_K2)
    with pytest.raises(ValueError):
        episode.step(RetrievalRLAction.SEARCH_K1)


def test_cannot_step_after_stop() -> None:
    episode = make_episode()
    episode.step(RetrievalRLAction.STOP)
    with pytest.raises(ValueError):
        episode.step(RetrievalRLAction.SEARCH_K1)
