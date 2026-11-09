from knowledgebench.evaluation.agent_grounding_grader import (
    grade_agent_grounding,
)
from knowledgebench.runs.agent_trace_schema import (
    AgentRunTrace,
)
from knowledgebench.tasks.agent_eval_schema import (
    AgentEvalTask,
)


def make_task() -> AgentEvalTask:
    return AgentEvalTask(
        task_id="t1",
        question="Where are failed jobs sent?",
        expected_answer="CIRRUS-DLQ",
        required_document_ids=[
            "org",
            "manual",
        ],
        max_reasonable_search_steps=2,
    )


def test_grounded_correct_answer() -> None:
    run = AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "find manual",
                    "retrieved_document_ids": [
                        "manual"
                    ],
                },
                {
                    "step_index": 1,
                    "action_type": "stop",
                    "answer": "CIRRUS-DLQ",
                },
            ],
        }
    )

    grade = grade_agent_grounding(
        task=make_task(),
        run=run,
        document_text_by_id={
            "manual": (
                "Failed jobs are sent to the "
                "CIRRUS-DLQ dead-letter queue."
            )
        },
    )

    assert grade.answer_correct is True
    assert grade.answer_grounded is True
    assert grade.grounded_but_wrong is False


def test_grounded_but_wrong_answer() -> None:
    run = AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "find manual",
                    "retrieved_document_ids": [
                        "manual"
                    ],
                },
                {
                    "step_index": 1,
                    "action_type": "stop",
                    "answer": "five times",
                },
            ],
        }
    )

    grade = grade_agent_grounding(
        task=make_task(),
        run=run,
        document_text_by_id={
            "manual": (
                "Jobs are retried five times before "
                "being sent to CIRRUS-DLQ."
            )
        },
    )

    assert grade.answer_correct is False
    assert grade.answer_grounded is True
    assert grade.grounded_but_wrong is True


def test_unsupported_wrong_answer() -> None:
    run = AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "find manual",
                    "retrieved_document_ids": [
                        "manual"
                    ],
                },
                {
                    "step_index": 1,
                    "action_type": "stop",
                    "answer": "UNKNOWN-QUEUE",
                },
            ],
        }
    )

    grade = grade_agent_grounding(
        task=make_task(),
        run=run,
        document_text_by_id={
            "manual": (
                "Jobs are retried five times before "
                "being sent to CIRRUS-DLQ."
            )
        },
    )

    assert grade.answer_correct is False
    assert grade.answer_grounded is False
    assert grade.grounded_but_wrong is False
