import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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

    split_counts = Counter(
        example.split.value
        for example in examples
        if example.split is not None
    )
    action_counts = Counter(
        example.target_action.value
        for example in examples
    )

    source_splits = defaultdict(set)
    for example in examples:
        if example.split is not None:
            source_splits[
                example.source_task_id
            ].add(example.split.value)

    leaked_sources = {
        source: sorted(splits)
        for source, splits in source_splits.items()
        if len(splits) > 1
    }

    print(
        "Phase 11 EXP-102 — Policy Dataset Audit"
    )
    print(f"examples={len(examples)}")
    print(
        f"split_counts={dict(split_counts)}"
    )
    print(
        f"action_counts={dict(action_counts)}"
    )
    print(
        f"source_tasks={len(source_splits)}"
    )
    print(
        f"leaked_sources={leaked_sources}"
    )

    if leaked_sources:
        raise ValueError(
            "source-task leakage across splits"
        )


if __name__ == "__main__":
    main()
