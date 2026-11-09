import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.graph.entity_resolution import (
    LexicalEntityResolver,
)
from knowledge_engine.graph.schema import ClaimGraph
from knowledgebench.tasks.graph_schema import EntityResolutionTask

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_entity_resolution_stress_tasks_v0.json"
)


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        EntityResolutionTask.model_validate(item)
        for item in json.loads(
            TASK_PATH.read_text(encoding="utf-8")
        )
    ]

    resolver = LexicalEntityResolver(graph)

    correct = 0
    resolvable_hits = 0
    resolvable_count = 0
    abstention_hits = 0
    abstention_count = 0
    false_positive_resolutions = 0

    for task in tasks:
        print(task.task_id)
        print(f"category={task.category}")
        print(f"question={task.question}")

        resolved_entity_id = None
        error = None

        try:
            result = resolver.resolve(
                task.question
            )
            resolved_entity_id = (
                result.entity_id
            )
            print(
                f"  resolved_entity_id={result.entity_id}"
            )
            print(
                f"  matched_surface={result.matched_surface!r}"
            )
            print(
                f"  match_type={result.match_type}"
            )
        except ValueError as exc:
            error = str(exc)
            print(
                f"  resolution_error={error}"
            )

        if task.should_resolve:
            resolvable_count += 1
            hit = (
                resolved_entity_id
                == task.expected_entity_id
            )
            resolvable_hits += int(hit)
        else:
            abstention_count += 1
            hit = resolved_entity_id is None
            abstention_hits += int(hit)
            false_positive_resolutions += int(
                resolved_entity_id is not None
            )

        correct += int(hit)
        print(f"  expected_success={hit}")
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "OverallAccuracy="
        f"{correct / task_count:.4f}"
    )
    print(
        "ResolvableEntityAccuracy="
        f"{resolvable_hits / resolvable_count:.4f}"
    )
    print(
        "AbstentionAccuracy="
        f"{abstention_hits / abstention_count:.4f}"
    )
    print(
        "FalsePositiveResolutionRate="
        f"{false_positive_resolutions / abstention_count:.4f}"
    )


if __name__ == "__main__":
    main()
