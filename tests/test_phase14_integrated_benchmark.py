"""Phase 14 integrated evaluation: judge gold only after results exist."""

import pytest

from scripts.run_phase14_integrated_benchmark import (
    evaluate_development_tasks,
    summarize,
)


def test_real_hard_benchmark_executes_no_model_download():
    reports = evaluate_development_tasks()
    assert len(reports) == 20
    assert {r["strategy"] for r in reports} == {"static", "auto"}
    assert {r["task_id"] for r in reports} == {
        f"kbv2-hard-{i:03d}" for i in range(1, 11)
    }
    assert all(r["retrieved_count"] > 0 for r in reports)
    assert all(r["steps"] >= 1 for r in reports)
    assert all(r["source_answer"] is None or r["citation_ids"] for r in reports)


def test_gold_and_abstention_metrics_are_not_treated_as_policy_inputs():
    reports = evaluate_development_tasks()
    summary = summarize(reports)
    for strategy in ("static", "auto"):
        data = summary[strategy]
        assert data["answerable_count"] == 6
        assert data["unanswerable_count"] == 4
        for key in (
            "mean_evidence_recall", "complete_support_rate",
            "extractive_answer_accuracy_on_answerable",
            "answerable_abstention_rate", "unanswerable_abstention_rate",
            "fallback_rate",
        ):
            assert 0 <= data[key] <= 1
        assert data["mean_search_calls"] >= 1
        assert data["mean_unique_docs"] >= 1


def test_static_and_auto_calls_are_not_mistaken_for_equal_budgets():
    rows = evaluate_development_tasks()
    static = [r for r in rows if r["strategy"] == "static"]
    auto = [r for r in rows if r["strategy"] == "auto"]
    assert all(r["steps"] == 1 and r["retrieved_count"] == 3 for r in static)
    assert any(r["fallback"] is not None for r in auto)


def test_missing_reports_rejected():
    with pytest.raises(ValueError, match="missing reports"):
        summarize([])
