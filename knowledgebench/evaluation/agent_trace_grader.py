from dataclasses import dataclass

from knowledgebench.runs.agent_trace_schema import (
    AgentActionType,
    AgentRunTrace,
)
from knowledgebench.tasks.agent_eval_schema import (
    AgentEvalTask,
)


def normalize_text(value: str) -> str:
    return " ".join(
        value.casefold().split()
    )


@dataclass(frozen=True)
class AgentTraceGrade:
    task_id: str
    search_steps: int
    repeated_searches: int
    required_evidence_coverage: float
    stopped: bool
    answer_correct: bool
    premature_stop: bool
    efficient_search: bool
    retrieved_required_evidence: bool


def grade_agent_trace(
    task: AgentEvalTask,
    run: AgentRunTrace,
) -> AgentTraceGrade:
    if task.task_id != run.task_id:
        raise ValueError(
            "task and run task_id must match"
        )

    search_steps = [
        step
        for step in run.steps
        if step.action_type == AgentActionType.SEARCH
    ]
    stop_steps = [
        step
        for step in run.steps
        if step.action_type == AgentActionType.STOP
    ]

    normalized_queries = [
        normalize_text(step.query or "")
        for step in search_steps
    ]
    repeated_searches = (
        len(normalized_queries)
        - len(set(normalized_queries))
    )

    retrieved_ids = {
        document_id
        for step in search_steps
        for document_id in step.retrieved_document_ids
    }
    required_ids = set(
        task.required_document_ids
    )

    required_evidence_coverage = (
        len(retrieved_ids & required_ids)
        / len(required_ids)
    )
    retrieved_required_evidence = (
        required_ids.issubset(retrieved_ids)
    )

    stopped = bool(stop_steps)
    final_answer = (
        stop_steps[0].answer
        if stop_steps
        else None
    )
    answer_correct = (
        final_answer is not None
        and normalize_text(final_answer)
        == normalize_text(task.expected_answer)
    )

    premature_stop = (
        stopped
        and not retrieved_required_evidence
    )

    efficient_search = (
        len(search_steps)
        <= task.max_reasonable_search_steps
        and repeated_searches == 0
    )

    return AgentTraceGrade(
        task_id=task.task_id,
        search_steps=len(search_steps),
        repeated_searches=repeated_searches,
        required_evidence_coverage=(
            required_evidence_coverage
        ),
        stopped=stopped,
        answer_correct=answer_correct,
        premature_stop=premature_stop,
        efficient_search=efficient_search,
        retrieved_required_evidence=(
            retrieved_required_evidence
        ),
    )



@dataclass(frozen=True)
class AgentTraceAggregateGrade:
    tasks: int
    answer_accuracy: float
    full_evidence_rate: float
    premature_stop_rate: float
    efficient_search_rate: float
    average_search_steps: float
    average_repeated_searches: float


def aggregate_agent_trace_grades(
    grades: list[AgentTraceGrade],
) -> AgentTraceAggregateGrade:
    if not grades:
        raise ValueError(
            "agent trace aggregation requires grades"
        )

    tasks = len(grades)

    return AgentTraceAggregateGrade(
        tasks=tasks,
        answer_accuracy=(
            sum(grade.answer_correct for grade in grades)
            / tasks
        ),
        full_evidence_rate=(
            sum(
                grade.retrieved_required_evidence
                for grade in grades
            )
            / tasks
        ),
        premature_stop_rate=(
            sum(grade.premature_stop for grade in grades)
            / tasks
        ),
        efficient_search_rate=(
            sum(grade.efficient_search for grade in grades)
            / tasks
        ),
        average_search_steps=(
            sum(grade.search_steps for grade in grades)
            / tasks
        ),
        average_repeated_searches=(
            sum(grade.repeated_searches for grade in grades)
            / tasks
        ),
    )
