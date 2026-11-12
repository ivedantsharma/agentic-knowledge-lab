from knowledge_engine.training.measured_policy_dataset import (
    MeasuredPolicyExample,
    evidence_family_leakage,
)


def test_no_leakage_for_disjoint_families() -> None:
    examples = [
        MeasuredPolicyExample(
            example_id="a",
            source_task_id="s1",
            evidence_family="family-a",
            split="train",
            question="Question A",
            target_action="SEARCH_HYBRID_K1",
            label_source="oracle",
        ),
        MeasuredPolicyExample(
            example_id="b",
            source_task_id="s2",
            evidence_family="family-b",
            split="heldout",
            question="Question B",
            target_action="SEARCH_HYBRID_K2",
            label_source="oracle",
        ),
    ]

    assert evidence_family_leakage(examples) == {}


def test_detects_family_leakage() -> None:
    examples = [
        MeasuredPolicyExample(
            example_id="a",
            source_task_id="s1",
            evidence_family="shared",
            split="train",
            question="Question A",
            target_action="SEARCH_HYBRID_K1",
            label_source="oracle",
        ),
        MeasuredPolicyExample(
            example_id="b",
            source_task_id="s2",
            evidence_family="shared",
            split="dev",
            question="Question B",
            target_action="SEARCH_HYBRID_K1",
            label_source="oracle",
        ),
    ]

    assert evidence_family_leakage(
        examples
    ) == {
        "shared": ("dev", "train")
    }
