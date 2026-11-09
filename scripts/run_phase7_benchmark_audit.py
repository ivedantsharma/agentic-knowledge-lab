import json
from pathlib import Path

from knowledgebench.documents.v2_schema import (
    KnowledgeBenchV2Document,
)
from knowledgebench.evaluation.v2_audit import (
    AUDIT_RULE_VERSION,
    audit_knowledgebench_v2,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
)


DOCUMENTS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_documents_v0.json"
)
TASKS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_tasks_v0.json"
)


def main() -> None:
    documents = [
        KnowledgeBenchV2Document.model_validate(item)
        for item in json.loads(
            DOCUMENTS_PATH.read_text(encoding="utf-8")
        )
    ]
    tasks = [
        KnowledgeBenchV2Task.model_validate(item)
        for item in json.loads(
            TASKS_PATH.read_text(encoding="utf-8")
        )
    ]

    report = audit_knowledgebench_v2(
        documents,
        tasks,
    )

    print("KnowledgeBench v2 Hard v0 — Integrity Audit")
    print(f"audit_rule_version={AUDIT_RULE_VERSION}")
    print(f"documents={report.document_count}")
    print(f"tasks={report.task_count}")
    print(f"answerable_tasks={report.answerable_tasks}")
    print(f"unanswerable_tasks={report.unanswerable_tasks}")
    print(
        f"role_reference_count={report.role_reference_count}"
    )

    print("challenge_counts")
    for challenge, count in report.challenge_counts.items():
        print(
            f"  {challenge}={count}"
        )

    print(
        "missing_document_references="
        f"{report.missing_document_references}"
    )
    print(
        "duplicate_document_ids="
        f"{report.duplicate_document_ids}"
    )
    print(
        "duplicate_task_ids="
        f"{report.duplicate_task_ids}"
    )
    print(
        "temporal_tasks_without_dated_evidence="
        f"{report.temporal_tasks_without_dated_evidence}"
    )
    print(
        "ambiguity_tasks_with_too_few_candidates="
        f"{report.ambiguity_tasks_with_too_few_candidates}"
    )
    print(f"passed={report.passed}")


if __name__ == "__main__":
    main()
