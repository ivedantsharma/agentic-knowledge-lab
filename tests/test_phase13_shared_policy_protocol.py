"""EXP-124 Gate B0: shared-action mechanics and policy visibility tests."""

import pytest

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.rl.shared_policy_protocol import (
    ACTION_NAMES,
    GAMMA,
    MAX_STEPS,
    PROTOCOL_ID,
    FixedKPolicy,
    run_shared_episode,
)
from scripts.run_phase12_family_disjoint_transfer import load_ranked_tasks


def test_action_vocabulary_is_one_explicit_protocol() -> None:
    assert PROTOCOL_ID == "EXP-124-common-bm25-v0"
    assert ACTION_NAMES == (
        "SEARCH_K1", "SEARCH_K2", "SEARCH_K3", "SEARCH_K5", "STOP"
    )
    assert "REFORMULATE" not in ACTION_NAMES
    assert GAMMA == 0.9
    assert MAX_STEPS == 6


@pytest.mark.parametrize("k", [1, 2, 3, 5])
def test_fixed_policy_runs_same_episode_reward_and_stop(k: int) -> None:
    result = run_shared_episode(
        policy=FixedKPolicy(k),
        question="Where is the answer?",
        ranked_ids=["support", "other", "another", "other2", "other3"],
        supporting_ids={"support"},
    )
    assert result.protocol_id == PROTOCOL_ID
    assert result.actions == (
        RetrievalRLAction(f"SEARCH_K{k}"), RetrievalRLAction.STOP
    )
    assert result.documents_returned == k
    assert result.final_observation.done
    assert result.discounted_return == pytest.approx(
        (2.0 - 0.1 * k) + GAMMA
    )


def test_gold_is_never_passed_to_policy_action_selection() -> None:
    class InspectPolicy:
        def __init__(self) -> None:
            self.seen = []

        def choose_action(self, observation):
            self.seen.append(observation)
            assert not hasattr(observation, "supporting_ids")
            assert not hasattr(observation, "expected_answer")
            assert not hasattr(observation, "reward")
            if not observation.retrieved_ids:
                return RetrievalRLAction.SEARCH_K2
            return RetrievalRLAction.STOP

    p1, p2 = InspectPolicy(), InspectPolicy()
    kwargs = {"question": "same query", "ranked_ids": ["a", "b", "c"]}
    a = run_shared_episode(policy=p1, supporting_ids={"a"}, **kwargs)
    b = run_shared_episode(policy=p2, supporting_ids={"c"}, **kwargs)
    assert p1.seen == p2.seen
    assert a.actions == b.actions
    assert a.discounted_return != b.discounted_return


def test_illegal_repeated_budget_is_rejected_before_environment_step() -> None:
    class IllegalPolicy:
        def choose_action(self, observation):
            return RetrievalRLAction.SEARCH_K1

    with pytest.raises(ValueError, match="illegal action"):
        run_shared_episode(
            policy=IllegalPolicy(),
            question="q", ranked_ids=["a", "b"],
            supporting_ids={"a"},
        )


def test_wrong_action_type_cannot_cast_historical_sft_labels() -> None:
    class OldSftPolicy:
        def choose_action(self, observation):
            return "SEARCH_HYBRID_K3"

    with pytest.raises(ValueError, match="non-contract action"):
        run_shared_episode(
            policy=OldSftPolicy(),
            question="q", ranked_ids=["a"],
            supporting_ids={"a"},
        )


def test_max_steps_forced_timeout_does_not_fake_stop() -> None:
    result = run_shared_episode(
        policy=FixedKPolicy(3),
        question="q", ranked_ids=["a", "b", "c"],
        supporting_ids={"c"},
        max_steps=1,
    )
    assert result.actions == (RetrievalRLAction.SEARCH_K3,)
    assert result.final_observation.done


def test_shared_protocol_runs_existing_route_tasks_as_development_only() -> None:
    tasks = load_ranked_tasks()
    assert len(tasks) == 12
    for task in tasks:
        result = run_shared_episode(
            policy=FixedKPolicy(3),
            question=task.question,
            ranked_ids=list(task.ranked_ids),
            supporting_ids=set(task.supporting_ids),
        )
        assert result.actions == (
            RetrievalRLAction.SEARCH_K3, RetrievalRLAction.STOP
        )
        assert result.documents_returned == 3


def test_fixed_policy_rejects_invalid_budget() -> None:
    with pytest.raises(ValueError, match="one of"):
        FixedKPolicy(4)
