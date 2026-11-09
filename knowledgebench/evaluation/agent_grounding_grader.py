from dataclasses import dataclass

from knowledgebench.evaluation.agent_trace_grader import (
    normalize_text,
)
from knowledgebench.runs.agent_trace_schema import (
    AgentActionType,
    AgentRunTrace,
)
from knowledgebench.tasks.agent_eval_schema import (
    AgentEvalTask,
)


@dataclass(frozen=True)
class AgentGroundingGrade:
    task_id: str
    stopped: bool
    answer_correct: bool
    answer_grounded: bool
    grounded_but_wrong: bool
    supporting_document_ids: list[str]


def grade_agent_grounding(
    *,
    task: AgentEvalTask,
    run: AgentRunTrace,
    document_text_by_id: dict[str, str],
) -> AgentGroundingGrade:
    if task.task_id != run.task_id:
        raise ValueError(
            "task and run task_id must match"
        )

    stop_steps = [
        step
        for step in run.steps
        if step.action_type == AgentActionType.STOP
    ]

    if not stop_steps:
        return AgentGroundingGrade(
            task_id=task.task_id,
            stopped=False,
            answer_correct=False,
            answer_grounded=False,
            grounded_but_wrong=False,
            supporting_document_ids=[],
        )

    answer = stop_steps[0].answer or ""
    normalized_answer = normalize_text(
        answer
    )

    consumed_ids = [
        document_id
        for step in run.steps
        if step.action_type == AgentActionType.SEARCH
        for document_id in step.retrieved_document_ids
    ]

    supporting_document_ids = [
        document_id
        for document_id in consumed_ids
        if (
            document_id in document_text_by_id
            and normalized_answer
            in normalize_text(
                document_text_by_id[document_id]
            )
        )
    ]

    answer_grounded = bool(
        supporting_document_ids
    )
    answer_correct = (
        normalized_answer
        == normalize_text(
            task.expected_answer
        )
    )

    return AgentGroundingGrade(
        task_id=task.task_id,
        stopped=True,
        answer_correct=answer_correct,
        answer_grounded=answer_grounded,
        grounded_but_wrong=(
            answer_grounded
            and not answer_correct
        ),
        supporting_document_ids=(
            supporting_document_ids
        ),
    )
