import pytest
from pydantic import ValidationError

from knowledgebench.evaluation.agent_trace_grader import (
    grade_agent_trace,
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
        question="What is the value?",
        expected_answer="six hours",
        required_document_ids=[
            "bridge",
            "policy",
        ],
        max_reasonable_search_steps=2,
    )


def test_ideal_trace_is_correct_and_efficient() -> None:
    run = AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "find bridge",
                    "retrieved_document_ids": [
                        "bridge"
                    ],
                },
                {
                    "step_index": 1,
                    "action_type": "search",
                    "query": "find policy",
                    "retrieved_document_ids": [
                        "policy"
                    ],
                },
                {
                    "step_index": 2,
                    "action_type": "stop",
                    "answer": "six hours",
                },
            ],
        }
    )

    grade = grade_agent_trace(
        make_task(),
        run,
    )

    assert grade.answer_correct is True
    assert grade.premature_stop is False
    assert grade.efficient_search is True
    assert grade.required_evidence_coverage == 1.0


def test_premature_stop_is_detected() -> None:
    run = AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "find bridge",
                    "retrieved_document_ids": [
                        "bridge"
                    ],
                },
                {
                    "step_index": 1,
                    "action_type": "stop",
                    "answer": "six hours",
                },
            ],
        }
    )

    grade = grade_agent_trace(
        make_task(),
        run,
    )

    assert grade.answer_correct is True
    assert grade.premature_stop is True
    assert grade.required_evidence_coverage == 0.5


def test_repeated_search_is_inefficient() -> None:
    run = AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "same query",
                    "retrieved_document_ids": [
                        "bridge"
                    ],
                },
                {
                    "step_index": 1,
                    "action_type": "search",
                    "query": "same query",
                    "retrieved_document_ids": [
                        "bridge"
                    ],
                },
                {
                    "step_index": 2,
                    "action_type": "search",
                    "query": "policy",
                    "retrieved_document_ids": [
                        "policy"
                    ],
                },
                {
                    "step_index": 3,
                    "action_type": "stop",
                    "answer": "six hours",
                },
            ],
        }
    )

    grade = grade_agent_trace(
        make_task(),
        run,
    )

    assert grade.repeated_searches == 1
    assert grade.efficient_search is False


def test_trace_schema_rejects_search_after_stop() -> None:
    with pytest.raises(ValidationError):
        AgentRunTrace.model_validate(
            {
                "task_id": "t1",
                "steps": [
                    {
                        "step_index": 0,
                        "action_type": "stop",
                        "answer": "six hours",
                    },
                    {
                        "step_index": 1,
                        "action_type": "search",
                        "query": "late search",
                        "retrieved_document_ids": [],
                    },
                ],
            }
        )
