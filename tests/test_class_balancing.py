from knowledge_engine.training.class_balancing import (
    action_counts,
    balanced_oversample,
)
from knowledge_engine.training.measured_policy_dataset import (
    MeasuredPolicyExample,
)


def make_example(
    example_id: str,
    action: str,
) -> MeasuredPolicyExample:
    return MeasuredPolicyExample(
        example_id=example_id,
        source_task_id=example_id,
        evidence_family=example_id,
        split="train",
        question=f"Question {example_id}",
        target_action=action,
        label_source="oracle",
    )


def test_balanced_oversample_equalizes_present_classes() -> None:
    examples = [
        make_example("a1", "SEARCH_HYBRID_K1"),
        make_example("a2", "SEARCH_HYBRID_K1"),
        make_example("b1", "SEARCH_HYBRID_K2"),
    ]

    balanced = balanced_oversample(
        examples
    )

    assert action_counts(balanced) == {
        "SEARCH_HYBRID_K1": 2,
        "SEARCH_HYBRID_K2": 2,
    }


def test_balanced_oversample_keeps_empty_input_empty() -> None:
    assert balanced_oversample([]) == []
