import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.graph.entity_resolution import (
    LexicalEntityResolver,
)
from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.traversal import ClaimGraphIndex
from knowledgebench.tasks.graph_schema import GraphTraversalTask

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_v0.json"
)
TASK_PATH = Path(
    "data/processed/phase6_graph_tasks_v0.json"
)


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )

    tasks = [
        GraphTraversalTask.model_validate(item)
        for item in json.loads(
            TASK_PATH.read_text(encoding="utf-8")
        )
    ]

    resolver = LexicalEntityResolver(graph)
    index = ClaimGraphIndex(graph)

    entity_hits = 0
    answer_hits = 0
    path_hits = 0
    provenance_hits = 0
    resolution_failures = 0

    for task in tasks:
        print(task.task_id)
        print(f"question={task.question}")

        try:
            resolution = resolver.resolve(
                task.question
            )
        except ValueError as exc:
            resolution_failures += 1
            print(
                f"  entity_resolution_error={exc}"
            )
            print()
            continue

        entity_hit = (
            resolution.entity_id
            == task.start_entity_id
        )
        entity_hits += int(entity_hit)

        print(
            f"  resolved_entity_id={resolution.entity_id}"
        )
        print(
            f"  matched_surface={resolution.matched_surface!r}"
        )
        print(
            f"  match_type={resolution.match_type}"
        )
        print(
            f"  entity_hit={entity_hit}"
        )

        result = index.traverse(
            start_entity_id=resolution.entity_id,
            relation_path=task.relation_path,
        )

        answer_hit = (
            result.final_value.casefold()
            == task.expected_answer.casefold()
        )
        path_hit = (
            result.claim_ids
            == task.expected_claim_ids
        )
        provenance_hit = (
            len(result.evidence)
            == len(task.expected_claim_ids)
            and all(
                item.document_id
                for item in result.evidence
            )
        )

        answer_hits += int(answer_hit)
        path_hits += int(path_hit)
        provenance_hits += int(
            provenance_hit
        )

        print(
            f"  claim_ids={result.claim_ids}"
        )
        print(
            f"  final_value={result.final_value!r}"
        )
        print(f"  answer_hit={answer_hit}")
        print(f"  path_hit={path_hit}")
        print(
            f"  provenance_hit={provenance_hit}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "EntityLinkAccuracy="
        f"{entity_hits / task_count:.4f}"
    )
    print(
        "EntityResolutionFailureRate="
        f"{resolution_failures / task_count:.4f}"
    )
    print(
        "AnswerAccuracy="
        f"{answer_hits / task_count:.4f}"
    )
    print(
        "PathAccuracy="
        f"{path_hits / task_count:.4f}"
    )
    print(
        "ProvenanceCoverage="
        f"{provenance_hits / task_count:.4f}"
    )


if __name__ == "__main__":
    main()
