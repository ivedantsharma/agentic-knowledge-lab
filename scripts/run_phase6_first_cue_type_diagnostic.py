import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.entity_type import (
    FirstCueEntityTypeInferer,
    LexicalEntityTypeInferer,
)
from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
)
from knowledgebench.tasks.graph_schema import (
    TypedEntityMentionResolutionTask,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
THRESHOLD = 0.39

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_auto_type_entity_tasks_v0.json"
)


def evaluate_policy(
    policy_name: str,
    inferer,
    ranker: SemanticEntityRanker,
    tasks: list[TypedEntityMentionResolutionTask],
) -> tuple[int, int, int, int, int]:
    type_hits = 0
    positive_hits = 0
    positive_count = 0
    abstention_hits = 0
    negative_count = 0

    print(f"Policy={policy_name}")

    for task in tasks:
        type_result = inferer.infer(
            task.mention_text
        )

        type_hit = (
            type_result.entity_type
            == task.expected_entity_type
        )
        type_hits += int(type_hit)

        if type_result.entity_type is None:
            accepted = False
            resolved_entity_id = None
            score = None
        else:
            ranking = ranker.rank_for_type(
                task.mention_text,
                type_result.entity_type,
            )
            top = ranking[0]
            score = float(top.score)
            accepted = score >= THRESHOLD
            resolved_entity_id = (
                top.entity_id
                if accepted
                else None
            )

        if task.should_resolve:
            positive_count += 1
            hit = (
                type_hit
                and accepted
                and resolved_entity_id
                == task.expected_entity_id
            )
            positive_hits += int(hit)
        else:
            negative_count += 1
            hit = not accepted
            abstention_hits += int(hit)

        print(task.task_id)
        print(
            f"  inferred_type={type_result.entity_type}"
        )
        print(
            f"  matched_cue={type_result.matched_cue!r}"
        )
        print(
            f"  resolved_entity_id={resolved_entity_id}"
        )
        print(f"  score={score}")
        print(f"  hit={hit}")

    return (
        type_hits,
        positive_hits,
        positive_count,
        abstention_hits,
        negative_count,
    )


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        TypedEntityMentionResolutionTask.model_validate(item)
        for item in json.loads(
            TASK_PATH.read_text(encoding="utf-8")
        )
    ]

    model = SentenceTransformer(MODEL_NAME)
    ranker = SemanticEntityRanker(
        graph=graph,
        model_name=MODEL_NAME,
        model=model,
    )

    baseline = evaluate_policy(
        "conflict-abstain",
        LexicalEntityTypeInferer(),
        ranker,
        tasks,
    )
    repaired = evaluate_policy(
        "first-cue",
        FirstCueEntityTypeInferer(),
        ranker,
        tasks,
    )

    task_count = len(tasks)

    print()
    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "BaselineTypeInferenceAccuracy="
        f"{baseline[0] / task_count:.4f}"
    )
    print(
        "FirstCueTypeInferenceAccuracy="
        f"{repaired[0] / task_count:.4f}"
    )
    print(
        "BaselineResolvableEntityAccuracy="
        f"{baseline[1] / baseline[2]:.4f}"
    )
    print(
        "FirstCueResolvableEntityAccuracy="
        f"{repaired[1] / repaired[2]:.4f}"
    )
    print(
        "BaselineAbstentionAccuracy="
        f"{baseline[3] / baseline[4]:.4f}"
    )
    print(
        "FirstCueAbstentionAccuracy="
        f"{repaired[3] / repaired[4]:.4f}"
    )


if __name__ == "__main__":
    main()
