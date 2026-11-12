import pytest

from knowledge_engine.training.policy_labeler import (
    label_budget_policy,
)


def test_labeler_maps_minimal_k_to_policy_action() -> None:
    label = label_budget_policy(
        ranked_ids=[
            "distractor",
            "target",
            "other",
        ],
        supporting_ids={"target"},
    )

    assert label.minimal_k == 2
    assert (
        label.action.value
        == "SEARCH_HYBRID_K2"
    )
    assert label.max_recall == 1.0


def test_labeler_keeps_smallest_k_at_plateau() -> None:
    label = label_budget_policy(
        ranked_ids=[
            "target",
            "other",
        ],
        supporting_ids={"target"},
    )

    assert label.minimal_k == 1


def test_labeler_rejects_unknown_budget() -> None:
    with pytest.raises(ValueError):
        label_budget_policy(
            ranked_ids=["target"],
            supporting_ids={"target"},
            candidate_ks=(1, 4),
        )
