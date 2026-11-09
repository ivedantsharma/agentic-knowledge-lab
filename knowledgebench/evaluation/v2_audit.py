from collections import Counter
from dataclasses import dataclass

from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document
AUDIT_RULE_VERSION = "temporal-v2"

from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
    KnowledgeChallenge,
)


@dataclass(frozen=True)
class KnowledgeBenchV2AuditReport:
    document_count: int
    task_count: int
    answerable_tasks: int
    unanswerable_tasks: int
    challenge_counts: dict[str, int]
    role_reference_count: int
    missing_document_references: list[str]
    duplicate_document_ids: list[str]
    duplicate_task_ids: list[str]
    temporal_tasks_without_dated_evidence: list[str]
    ambiguity_tasks_with_too_few_candidates: list[str]

    @property
    def passed(self) -> bool:
        return not any(
            [
                self.missing_document_references,
                self.duplicate_document_ids,
                self.duplicate_task_ids,
                self.temporal_tasks_without_dated_evidence,
                self.ambiguity_tasks_with_too_few_candidates,
            ]
        )


def _duplicates(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(
        value
        for value, count in counts.items()
        if count > 1
    )


def audit_knowledgebench_v2(
    documents: list[KnowledgeBenchV2Document],
    tasks: list[KnowledgeBenchV2Task],
) -> KnowledgeBenchV2AuditReport:
    document_ids = [
        document.document_id
        for document in documents
    ]
    task_ids = [
        task.task_id
        for task in tasks
    ]
    document_by_id = {
        document.document_id: document
        for document in documents
    }

    missing_references: set[str] = set()
    role_reference_count = 0

    for task in tasks:
        role_sets = [
            task.supporting_document_ids,
            task.distractor_document_ids,
            task.contradicting_document_ids,
            task.stale_document_ids,
            task.ambiguity_candidate_document_ids,
        ]

        for role_ids in role_sets:
            role_reference_count += len(role_ids)
            missing_references.update(
                role_ids - set(document_ids)
            )

    challenge_counts = {
        challenge.value: sum(
            challenge in task.challenge_types
            for task in tasks
        )
        for challenge in KnowledgeChallenge
    }

    temporal_failures: list[str] = []
    for task in tasks:
        if KnowledgeChallenge.STALE_KNOWLEDGE not in task.challenge_types:
            continue

        stale_documents = [
            document_by_id[document_id]
            for document_id in task.stale_document_ids
            if document_id in document_by_id
        ]
        supporting_documents = [
            document_by_id[document_id]
            for document_id in task.supporting_document_ids
            if document_id in document_by_id
        ]

        has_dated_stale_evidence = (
            bool(stale_documents)
            and all(
                document.effective_at is not None
                for document in stale_documents
            )
        )
        has_dated_current_support = any(
            document.effective_at is not None
            for document in supporting_documents
        )

        if (
            not has_dated_stale_evidence
            or not has_dated_current_support
        ):
            temporal_failures.append(
                task.task_id
            )

    ambiguity_failures = [
        task.task_id
        for task in tasks
        if (
            KnowledgeChallenge.AMBIGUITY in task.challenge_types
            and len(task.ambiguity_candidate_document_ids) < 2
        )
    ]

    return KnowledgeBenchV2AuditReport(
        document_count=len(documents),
        task_count=len(tasks),
        answerable_tasks=sum(
            task.should_answer
            for task in tasks
        ),
        unanswerable_tasks=sum(
            not task.should_answer
            for task in tasks
        ),
        challenge_counts=challenge_counts,
        role_reference_count=role_reference_count,
        missing_document_references=sorted(
            missing_references
        ),
        duplicate_document_ids=_duplicates(
            document_ids
        ),
        duplicate_task_ids=_duplicates(
            task_ids
        ),
        temporal_tasks_without_dated_evidence=(
            temporal_failures
        ),
        ambiguity_tasks_with_too_few_candidates=(
            ambiguity_failures
        ),
    )
