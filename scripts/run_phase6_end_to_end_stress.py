import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.hybrid_entity_resolution import (
    HybridEntityResolver,
)
from knowledge_engine.graph.path_search import (
    SemanticGraphPathRanker,
)
from knowledge_engine.graph.qa import ClaimGraphQAEngine
from knowledge_engine.graph.schema import ClaimGraph
from knowledgebench.tasks.graph_schema import (
    EndToEndGraphQATask,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
ENTITY_THRESHOLD = 0.39

GRAPH_PATH = Path(
    "data/processed/phase6_branching_claim_graph_v0.json"
)
TASK_PATH = Path(
    "data/processed/phase6_end_to_end_stress_tasks_v0.json"
)


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        EndToEndGraphQATask.model_validate(item)
        for item in json.loads(
            TASK_PATH.read_text(encoding="utf-8")
        )
    ]

    model = SentenceTransformer(MODEL_NAME)

    entity_resolver = HybridEntityResolver(
        graph=graph,
        model_name=MODEL_NAME,
        threshold=ENTITY_THRESHOLD,
        model=model,
    )
    path_ranker = SemanticGraphPathRanker(
        model_name=MODEL_NAME,
        model=model,
    )
    engine = ClaimGraphQAEngine(
        graph=graph,
        path_ranker=path_ranker,
        max_hops=3,
        entity_resolver=entity_resolver,
    )

    answerable_count = 0
    answerable_hits = 0
    entity_hits = 0
    path_hits = 0
    answer_hits = 0
    provenance_hits = 0

    abstention_count = 0
    abstention_hits = 0
    false_positive_answers = 0

    for task in tasks:
        print(task.task_id)
        print(f"category={task.category}")
        print(f"question={task.question}")

        try:
            result = engine.answer(
                task.question
            )
        except ValueError as exc:
            result = None
            print("  system_result=ABSTAIN")
            print(f"  reason={exc}")

        if task.should_answer:
            answerable_count += 1

            if result is None:
                print("  entity_hit=False")
                print("  path_hit=False")
                print("  answer_hit=False")
                print("  provenance_hit=False")
                print("  end_to_end_hit=False")
                print()
                continue

            entity_hit = (
                result.entity_resolution.entity_id
                == task.expected_entity_id
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
                    item.document_id
                    for item in result.evidence
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
            answerable_hits += int(
                end_to_end_hit
            )

            print(
                "  resolved_entity_id="
                f"{result.entity_resolution.entity_id}"
            )
            print(
                "  entity_match_type="
                f"{result.entity_resolution.match_type}"
            )
            print(
                f"  selected_relations={result.relation_path}"
            )
            print(
                f"  answer={result.answer!r}"
            )
            print(
                f"  top_path_score={result.top_path_score:.6f}"
            )
            if result.path_score_margin is None:
                print("  path_score_margin=None")
            else:
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
        else:
            abstention_count += 1
            abstained = result is None
            abstention_hits += int(
                abstained
            )
            false_positive_answers += int(
                not abstained
            )

            if result is not None:
                print(
                    "  false_positive_entity="
                    f"{result.entity_resolution.entity_id}"
                )
                print(
                    f"  false_positive_answer={result.answer!r}"
                )

            print(
                f"  abstention_hit={abstained}"
            )

        print()

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(
        "AnswerableEndToEndSuccessRate="
        f"{answerable_hits / answerable_count:.4f}"
    )
    print(
        "EntityResolutionAccuracy="
        f"{entity_hits / answerable_count:.4f}"
    )
    print(
        "PathSelectionAccuracy="
        f"{path_hits / answerable_count:.4f}"
    )
    print(
        "AnswerAccuracy="
        f"{answer_hits / answerable_count:.4f}"
    )
    print(
        "ProvenanceCoverage="
        f"{provenance_hits / answerable_count:.4f}"
    )
    print(
        "AbstentionAccuracy="
        f"{abstention_hits / abstention_count:.4f}"
    )
    print(
        "FalsePositiveAnswerRate="
        f"{false_positive_answers / abstention_count:.4f}"
    )


if __name__ == "__main__":
    main()
