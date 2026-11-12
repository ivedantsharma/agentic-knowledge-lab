from knowledge_engine.training.policy_dataset_audit import (
    audit_action_source_support,
)
from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyExample,
)


def test_source_support_detects_cross_source_class() -> None:
    examples = [
        RetrievalPolicyExample(
            example_id="a",
            source_task_id="source-a",
            question="Question A",
            target_action="SEARCH_HYBRID_K1",
            split="train",
        ),
        RetrievalPolicyExample(
            example_id="b",
            source_task_id="source-b",
            question="Question B",
            target_action="SEARCH_HYBRID_K1",
            split="heldout",
        ),
    ]

    reports = audit_action_source_support(
        examples
    )
    k1 = next(
        report
        for report in reports
        if report.action.value
        == "SEARCH_HYBRID_K1"
    )

    assert k1.source_count == 2
    assert (
        k1.supports_source_disjoint_evaluation
        is True
    )


def test_source_support_reports_absent_class() -> None:
    reports = audit_action_source_support([])

    assert all(
        report.source_count == 0
        for report in reports
    )
