from knowledgebench.evaluation.evidence_path_grader import (
    grade_evidence_path,
)
from knowledgebench.runs.agent_trace_schema import (
    AgentRunTrace,
)
from knowledgebench.tasks.multihop_schema import (
    MultiHopTask,
)


def make_task() -> MultiHopTask:
    return MultiHopTask.model_validate(
        {
            "task_id": "t1",
            "question": "What is the final value?",
            "expected_answer": "six hours",
            "hops": [
                {
                    "hop_index": 0,
                    "query": "find bridge",
                    "expected_document_id": "bridge",
                    "expected_fact": "service",
                },
                {
                    "hop_index": 1,
                    "query": "find policy",
                    "expected_document_id": "policy",
                    "expected_fact": "six hours",
                },
            ],
        }
    )


def make_run(
    consumed: list[str],
) -> AgentRunTrace:
    steps = [
        {
            "step_index": index,
            "action_type": "search",
            "query": f"q{index}",
            "retrieved_document_ids": [document_id],
        }
        for index, document_id in enumerate(consumed)
    ]
    steps.append(
        {
            "step_index": len(steps),
            "action_type": "stop",
            "answer": "six hours",
        }
    )

    return AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": steps,
        }
    )


def test_exact_path_match() -> None:
    grade = grade_evidence_path(
        task=make_task(),
        run=make_run(
            ["bridge", "policy"]
        ),
    )

    assert grade.path_coverage == 1.0
    assert grade.ordered_path_complete is True
    assert grade.exact_path_match is True
    assert grade.extra_documents == 0


def test_extra_document_preserves_ordered_completion() -> None:
    grade = grade_evidence_path(
        task=make_task(),
        run=make_run(
            [
                "bridge",
                "distractor",
                "policy",
            ]
        ),
    )

    assert grade.path_coverage == 1.0
    assert grade.ordered_path_complete is True
    assert grade.exact_path_match is False
    assert grade.extra_documents == 1


def test_wrong_order_fails_ordered_path() -> None:
    grade = grade_evidence_path(
        task=make_task(),
        run=make_run(
            ["policy", "bridge"]
        ),
    )

    assert grade.path_coverage == 1.0
    assert grade.ordered_path_complete is False
    assert grade.exact_path_match is False


def test_incomplete_path_reports_partial_coverage() -> None:
    grade = grade_evidence_path(
        task=make_task(),
        run=make_run(
            ["bridge"]
        ),
    )

    assert grade.path_coverage == 0.5
    assert grade.ordered_path_complete is False
    assert grade.exact_path_match is False
