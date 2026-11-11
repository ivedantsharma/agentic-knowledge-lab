from knowledgebench.evaluation.budget_oracle import (
    evaluate_budget_oracle,
    minimal_k_for_max_recall,
)


def test_minimal_k_for_max_recall() -> None:
    result = minimal_k_for_max_recall(
        task_id="t1",
        ranked_ids=["a", "x", "b", "y"],
        supporting_ids={"a", "b"},
        candidate_ks=(1, 2, 3, 4),
    )

    assert result.max_recall == 1.0
    assert result.minimal_k_for_max_recall == 3


def test_budget_oracle_aggregates_minimal_k() -> None:
    first = minimal_k_for_max_recall(
        task_id="t1",
        ranked_ids=["a", "x"],
        supporting_ids={"a"},
        candidate_ks=(1, 2),
    )
    second = minimal_k_for_max_recall(
        task_id="t2",
        ranked_ids=["x", "b"],
        supporting_ids={"b"},
        candidate_ks=(1, 2),
    )

    report = evaluate_budget_oracle(
        [first, second]
    )

    assert report.mean_minimal_k == 1.5
    assert report.max_required_k == 2
