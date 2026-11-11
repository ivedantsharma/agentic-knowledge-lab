import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.routing.query_features import (
    extract_query_features,
)
from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
)

TASKS_PATH = Path(
    "data/processed/knowledgebench_v2_hard_tasks_v0.json"
)

WINNERS = {
    "kbv2-hard-001": ["dense"],
    "kbv2-hard-002": ["bm25"],
    "kbv2-hard-005": ["bm25"],
    "kbv2-hard-006": [
        "bm25",
        "dense",
        "hybrid_rrf",
    ],
    "kbv2-hard-007": [
        "bm25",
        "dense",
        "hybrid_rrf",
    ],
    "kbv2-hard-010": [
        "dense",
        "hybrid_rrf",
    ],
}


def load_tasks() -> list[KnowledgeBenchV2Task]:
    return [
        KnowledgeBenchV2Task.model_validate(item)
        for item in json.loads(
            TASKS_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def main() -> None:
    tasks = [
        task
        for task in load_tasks()
        if task.should_answer
    ]

    print(
        "Phase 10 EXP-094 — Query Feature "
        "Diagnostic for Retriever Routing"
    )
    print()

    for task in tasks:
        features = extract_query_features(
            task.question
        )

        print(task.task_id)
        print(
            f"  winners={WINNERS[task.task_id]}"
        )
        print(
            f"  question={task.question!r}"
        )
        print(
            f"  token_count={features.token_count}"
        )
        print(
            "  capitalized_token_count="
            f"{features.capitalized_token_count}"
        )
        print(
            "  temporal_cue_count="
            f"{features.temporal_cue_count}"
        )
        print(
            "  relational_phrase_count="
            f"{features.relational_phrase_count}"
        )
        print(
            "  has_explicit_current_cue="
            f"{features.has_explicit_current_cue}"
        )
        print(
            "  has_multi_relation_proxy="
            f"{features.has_multi_relation_proxy}"
        )
        print()


if __name__ == "__main__":
    main()
