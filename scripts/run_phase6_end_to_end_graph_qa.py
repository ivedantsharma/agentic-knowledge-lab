import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.path_search import (
    SemanticGraphPathRanker,
)
from knowledge_engine.graph.qa import (
    ClaimGraphQAEngine,
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
    path_ranker = SemanticGraphPathRanker(
        model_name=MODEL_NAME,
        model=model,
    )
    engine = ClaimGraphQAEngine(
        graph=graph,
        path_ranker=path_ranker,
        max_hops=3,
    )

    entity_hits = 0
    path_hits = 0
    answer_hits = 0
    provenance_hits = 0
    end_to_end_hits = 0
    margins: list[float] = []

    for task in tasks:
        print(task.task_id)
        print(f"question={task.question}")

        try:
            result = engine.answer(
                task.question
            )
        except ValueError as exc:
            print(f"  error={exc}")
            print("  end_to_end_hit=False")
            print()
            continue

        entity_hit = (
            result.entity_resolution.entity_id
            == task.start_entity_id
        )
        path_hit = (
            result.claim_ids
            == task.expected_claim_ids
        )
        answer_hit = (
            result.answer.casefold()
            == task.expected_answer.casefold()
        )
        provenance_hit = (
            len(result.evidence)
            == len(result.claim_ids)
            and all(
                evidence.document_id
                for evidence in result.evidence
            )
        )
        end_to_end_hit = all(
            [
                entity_hit,
                path_hit,
                answer_hit,
                provenance_hit,
            ]
        )

        entity_hits += int(entity_hit)
        path_hits += int(path_hit)
        answer_hits += int(answer_hit)
        provenance_hits += int(
            provenance_hit
        )
        end_to_end_hits += int(
            end_to_end_hit
        )

        if result.path_score_margin is not None:
            margins.append(
                result.path_score_margin
            )

        print(
            "  resolved_entity_id="
            f"{result.entity_resolution.entity_id}"
        )
        print(
            "  matched_surface="
            f"{result.entity_resolution.matched_surface!r}"
        )
        print(
            f"  candidate_paths={result.candidate_path_count}"
        )
        print(
            f"  selected_relations={result.relation_path}"
        )
        print(
            f"  selected_claim_ids={result.claim_ids}"
        )
        print(f"  answer={result.answer!r}")
        print(
            "  evidence_documents="
            f"{[item.document_id for item in result.evidence]}"
        )
        print(
            f"  top_path_score={result.top_path_score:.6f}"
        )
        if result.second_path_score is None:
            print("  second_path_score=None")
            print("  path_score_margin=None")
        else:
            print(
                "  second_path_score="
                f"{result.second_path_score:.6f}"
            )
            print(
                "  path_score_margin="
                f"{result.path_score_margin:.6f}"
            )
        print(f"  entity_hit={entity_hit}")
        print(f"  path_hit={path_hit}")
        print(f"  answer_hit={answer_hit}")
        print(
            f"  provenance_hit={provenance_hit}"
        )
        print(
            f"  end_to_end_hit={end_to_end_hit}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "EntityResolutionAccuracy="
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
    print(
        "EndToEndSuccessRate="
        f"{end_to_end_hits / task_count:.4f}"
    )
    print(
        "AvgPathScoreMargin="
        f"{sum(margins) / len(margins):.6f}"
        if margins
        else "AvgPathScoreMargin=None"
    )


if __name__ == "__main__":
    main()
