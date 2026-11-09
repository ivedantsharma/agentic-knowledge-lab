from knowledgebench.evaluation.relation_alignment_grader import (
    grade_relation_alignment,
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
            "question": "Where are failed jobs sent?",
            "expected_answer": "CIRRUS-DLQ",
            "hops": [
                {
                    "hop_index": 0,
                    "query": "Which platform?",
                    "expected_document_id": "org",
                    "expected_fact": "Cirrus",
                    "extraction_pattern": (
                        "maintains the (.+?) worker platform"
                    ),
                },
                {
                    "hop_index": 1,
                    "query": "Where are exhausted jobs sent?",
                    "expected_document_id": "manual",
                    "expected_fact": "CIRRUS-DLQ",
                    "extraction_pattern": (
                        "sent to the (.+?) dead-letter queue"
                    ),
                },
            ],
        }
    )


def make_run(answer: str) -> AgentRunTrace:
    return AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "Which platform?",
                    "retrieved_document_ids": ["org"],
                },
                {
                    "step_index": 1,
                    "action_type": "search",
                    "query": "Where sent?",
                    "retrieved_document_ids": ["manual"],
                },
                {
                    "step_index": 2,
                    "action_type": "stop",
                    "answer": answer,
                },
            ],
        }
    )


def test_correct_relation_answer_is_aligned() -> None:
    grade = grade_relation_alignment(
        task=make_task(),
        run=make_run("CIRRUS-DLQ"),
        document_text_by_id={
            "manual": (
                "Jobs that exhaust retries are sent to the "
                "CIRRUS-DLQ dead-letter queue."
            )
        },
    )

    assert grade.final_evidence_consumed is True
    assert grade.extracted_relation_answer == "CIRRUS-DLQ"
    assert grade.relation_aligned is True


def test_grounded_wrong_relation_is_not_aligned() -> None:
    grade = grade_relation_alignment(
        task=make_task(),
        run=make_run("five times"),
        document_text_by_id={
            "manual": (
                "Failed jobs are retried five times. "
                "Jobs that exhaust retries are sent to the "
                "CIRRUS-DLQ dead-letter queue."
            )
        },
    )

    assert grade.final_evidence_consumed is True
    assert grade.extracted_relation_answer == "CIRRUS-DLQ"
    assert grade.relation_aligned is False


def test_missing_final_evidence_cannot_be_aligned() -> None:
    run = AgentRunTrace.model_validate(
        {
            "task_id": "t1",
            "steps": [
                {
                    "step_index": 0,
                    "action_type": "search",
                    "query": "Which platform?",
                    "retrieved_document_ids": ["org"],
                },
                {
                    "step_index": 1,
                    "action_type": "stop",
                    "answer": "CIRRUS-DLQ",
                },
            ],
        }
    )

    grade = grade_relation_alignment(
        task=make_task(),
        run=run,
        document_text_by_id={
            "manual": (
                "Jobs that exhaust retries are sent to the "
                "CIRRUS-DLQ dead-letter queue."
            )
        },
    )

    assert grade.final_evidence_consumed is False
    assert grade.relation_aligned is False
