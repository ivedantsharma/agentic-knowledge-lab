import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.qa import (
    GraphQAPipeline,
)
from knowledge_engine.graph.schema import ClaimGraph
from knowledgebench.tasks.graph_schema import (
    GraphTraversalTask,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GRAPH_PATH = Path(
    "data/processed/phase6_branching_claim_graph_v0.json"
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

    model = SentenceTransformer(MODEL_NAME)
    pipeline = GraphQAPipeline(
        graph=graph,
        model_name=MODEL_NAME,
        model=model,
        max_hops=3,
    )

    entity_hits = 0
    path_hits = 0
    answer_hits = 0
    provenance_hits = 0

    for task in tasks:
        result = pipeline.answer(
            task.question
        )

        entity_hit = (
            result.entity_resolution.entity_id
            == task.start_entity_id
        )
        path_hit = (
            result.claim_ids
            == task.expected_claim_ids
        )
        answer_hit = (
            result.final_value.casefold()
            == task.expected_answer.casefold()
        )
        provenance_hit = (
            len(result.evidence)
            == len(task.expected_claim_ids)
            and all(
                item.document_id
                for item in result.evidence
            )
        )

        entity_hits += int(entity_hit)
        path_hits += int(path_hit)
        answer_hits += int(answer_hit)
        provenance_hits += int(
            provenance_hit
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(
            "  resolved_entity_id="
            f"{result.entity_resolution.entity_id}"
        )
        print(
            "  matched_surface="
            f"{result.entity_resolution.matched_surface!r}"
        )
        print(
            "  selected_relations="
            f"{result.selected_path.candidate.relation_path}"
        )
        print(
            "  path_score="
            f"{result.selected_path.score:.6f}"
        )
        print(
            f"  claim_ids={result.claim_ids}"
        )
        print(
            f"  final_value={result.final_value!r}"
        )
        print(
            "  evidence_documents="
            f"{[item.document_id for item in result.evidence]}"
        )
        print(f"  entity_hit={entity_hit}")
        print(f"  path_hit={path_hit}")
        print(f"  answer_hit={answer_hit}")
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
        "PathSelectionAccuracy="
        f"{path_hits / task_count:.4f}"
    )
    print(
        "AnswerAccuracy="
        f"{answer_hits / task_count:.4f}"
    )
    print(
        "ProvenanceCoverage="
        f"{provenance_hits / task_count:.4f}"
    )


if __name__ == "__main__":
    main()
