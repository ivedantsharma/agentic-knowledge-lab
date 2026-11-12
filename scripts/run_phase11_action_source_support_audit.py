import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.training.policy_dataset_audit import (
    audit_action_source_support,
)
from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyExample,
)


DATA_PATH = Path(
    "data/processed/phase11_policy_dataset_v0.json"
)


def main() -> None:
    examples = [
        RetrievalPolicyExample.model_validate(item)
        for item in json.loads(
            DATA_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]

    reports = audit_action_source_support(
        examples
    )

    print(
        "Phase 11 EXP-106 — Action-Class "
        "Source-Support Audit"
    )
    print()

    evaluable_count = 0

    for report in reports:
        print(report.action.value)
        print(
            f"  source_count={report.source_count}"
        )
        print(
            "  sources="
            f"{list(report.source_task_ids)}"
        )
        print(
            "  split_sources="
            f"{report.split_source_task_ids}"
        )
        print(
            "  source_disjoint_evaluable="
            f"{report.supports_source_disjoint_evaluation}"
        )
        print()

        evaluable_count += int(
            report.supports_source_disjoint_evaluation
        )

    print("Summary")
    print(
        "  action_classes="
        f"{len(reports)}"
    )
    print(
        "  source_disjoint_evaluable_classes="
        f"{evaluable_count}"
    )
    print(
        "  insufficient_classes="
        f"{len(reports) - evaluable_count}"
    )


if __name__ == "__main__":
    main()
