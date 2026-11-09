import re
from dataclasses import dataclass

from knowledgebench.evaluation.agent_trace_grader import (
    normalize_text,
)
from knowledgebench.runs.agent_trace_schema import (
    AgentActionType,
    AgentRunTrace,
)
from knowledgebench.tasks.multihop_schema import (
    MultiHopTask,
)


@dataclass(frozen=True)
class RelationAlignmentGrade:
    task_id: str
    stopped: bool
    final_evidence_consumed: bool
    extracted_relation_answer: str | None
    relation_aligned: bool


def grade_relation_alignment(
    *,
    task: MultiHopTask,
    run: AgentRunTrace,
    document_text_by_id: dict[str, str],
) -> RelationAlignmentGrade:
    if task.task_id != run.task_id:
        raise ValueError(
            "task and run task_id must match"
        )

    final_hop = task.hops[-1]

    if final_hop.extraction_pattern is None:
        raise ValueError(
            "final hop requires extraction_pattern"
        )

    stop_steps = [
        step
        for step in run.steps
        if step.action_type == AgentActionType.STOP
    ]
    if not stop_steps:
        return RelationAlignmentGrade(
            task_id=task.task_id,
            stopped=False,
            final_evidence_consumed=False,
            extracted_relation_answer=None,
            relation_aligned=False,
        )

    consumed_ids = [
        document_id
        for step in run.steps
        if step.action_type == AgentActionType.SEARCH
        for document_id in step.retrieved_document_ids
    ]
    final_evidence_consumed = (
        final_hop.expected_document_id
        in consumed_ids
    )

    if not final_evidence_consumed:
        return RelationAlignmentGrade(
            task_id=task.task_id,
            stopped=True,
            final_evidence_consumed=False,
            extracted_relation_answer=None,
            relation_aligned=False,
        )

    evidence_text = document_text_by_id[
        final_hop.expected_document_id
    ]
    match = re.search(
        final_hop.extraction_pattern,
        evidence_text,
        flags=re.IGNORECASE,
    )

    if match is None or match.lastindex is None:
        return RelationAlignmentGrade(
            task_id=task.task_id,
            stopped=True,
            final_evidence_consumed=True,
            extracted_relation_answer=None,
            relation_aligned=False,
        )

    extracted_answer = match.group(1).strip()
    stopped_answer = stop_steps[0].answer or ""

    return RelationAlignmentGrade(
        task_id=task.task_id,
        stopped=True,
        final_evidence_consumed=True,
        extracted_relation_answer=(
            extracted_answer
        ),
        relation_aligned=(
            normalize_text(stopped_answer)
            == normalize_text(extracted_answer)
        ),
    )
