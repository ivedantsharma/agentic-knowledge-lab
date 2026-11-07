from knowledge_engine.agent.evaluation import (
    PlannerTaskResult,
    aggregate_planner_results,
    answer_matches,
)


def test_answer_matches_allows_grounded_longer_span() -> None:
    assert answer_matches(
        "CIRRUS-DLQ dead-letter queue",
        "CIRRUS-DLQ",
    )


def test_premature_stop_requires_missing_final_evidence() -> None:
    result = PlannerTaskResult(
        task_id="task-1",
        expected_answer="answer",
        final_answer="wrong",
        stopped=True,
        planner_failed=False,
        max_steps_exhausted=False,
        search_steps=1,
        retrieved_document_ids=["intermediate"],
        final_evidence_document_id="final",
    )

    assert result.premature_stop is True


def test_aggregate_planner_metrics() -> None:
    results = [
        PlannerTaskResult(
            task_id="task-1",
            expected_answer="alpha",
            final_answer="alpha",
            stopped=True,
            planner_failed=False,
            max_steps_exhausted=False,
            search_steps=2,
            retrieved_document_ids=["a", "final-a"],
            final_evidence_document_id="final-a",
        ),
        PlannerTaskResult(
            task_id="task-2",
            expected_answer="beta",
            final_answer=None,
            stopped=False,
            planner_failed=True,
            max_steps_exhausted=False,
            search_steps=1,
            retrieved_document_ids=["b"],
            final_evidence_document_id="final-b",
        ),
    ]

    metrics = aggregate_planner_results(results)

    assert metrics.tasks == 2
    assert metrics.answer_accuracy == 0.5
    assert metrics.planner_failure_rate == 0.5
    assert metrics.stopped_rate == 0.5
    assert metrics.stop_precision == 1.0
    assert metrics.premature_stop_rate == 0.0
    assert metrics.search_success_rate == 0.5
    assert metrics.average_search_steps == 1.5
    assert metrics.max_step_exhaustion_rate == 0.0
