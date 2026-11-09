from dataclasses import dataclass

from knowledgebench.runs.agent_trace_schema import (
    AgentActionType,
    AgentRunTrace,
)
from knowledgebench.tasks.multihop_schema import (
    MultiHopTask,
)


@dataclass(frozen=True)
class EvidencePathGrade:
    task_id: str
    expected_path: list[str]
    consumed_path: list[str]
    ordered_path_complete: bool
    exact_path_match: bool
    path_coverage: float
    extra_documents: int


def _is_subsequence(
    expected: list[str],
    observed: list[str],
) -> bool:
    if not expected:
        return True

    expected_index = 0

    for document_id in observed:
        if document_id == expected[expected_index]:
            expected_index += 1
            if expected_index == len(expected):
                return True

    return False


def grade_evidence_path(
    *,
    task: MultiHopTask,
    run: AgentRunTrace,
) -> EvidencePathGrade:
    if task.task_id != run.task_id:
        raise ValueError(
            "task and run task_id must match"
        )

    expected_path = [
        hop.expected_document_id
        for hop in task.hops
    ]
    consumed_path = [
        document_id
        for step in run.steps
        if step.action_type == AgentActionType.SEARCH
        for document_id in step.retrieved_document_ids
    ]

    expected_set = set(expected_path)
    consumed_set = set(consumed_path)

    path_coverage = (
        len(expected_set & consumed_set)
        / len(expected_set)
    )

    extra_documents = sum(
        document_id not in expected_set
        for document_id in consumed_path
    )

    return EvidencePathGrade(
        task_id=task.task_id,
        expected_path=expected_path,
        consumed_path=consumed_path,
        ordered_path_complete=_is_subsequence(
            expected_path,
            consumed_path,
        ),
        exact_path_match=(
            consumed_path == expected_path
        ),
        path_coverage=path_coverage,
        extra_documents=extra_documents,
    )
