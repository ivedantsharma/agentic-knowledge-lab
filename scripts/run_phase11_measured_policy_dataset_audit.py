import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.training.measured_policy_dataset import (
    MeasuredPolicyExample,
    evidence_family_leakage,
)

DATA_PATH = Path(
    "data/processed/phase11_policy_dataset_v1.json"
)


def main() -> None:
    examples = [
        MeasuredPolicyExample.model_validate(item)
        for item in json.loads(
            DATA_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]

    split_counts = Counter(
        example.split.value
        for example in examples
    )
    action_counts = Counter(
        example.target_action.value
        for example in examples
    )

    family_splits = defaultdict(set)
    for example in examples:
        family_splits[
            example.evidence_family
        ].add(
            example.split.value
        )

    leakage = evidence_family_leakage(
        examples
    )

    print(
        "Phase 11 EXP-108 — Measured Policy "
        "Dataset v1 Audit"
    )
    print(f"examples={len(examples)}")
    print(
        f"split_counts={dict(split_counts)}"
    )
    print(
        f"action_counts={dict(action_counts)}"
    )
    print(
        "evidence_families="
        f"{len(family_splits)}"
    )
    print(
        f"family_leakage={leakage}"
    )
    print()

    print("Evidence family splits")
    for family, splits in sorted(
        family_splits.items()
    ):
        print(
            f"  {family}: "
            f"{sorted(splits)}"
        )

    if leakage:
        raise ValueError(
            "evidence-family leakage across splits"
        )


if __name__ == "__main__":
    main()
