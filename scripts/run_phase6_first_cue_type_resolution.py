import json
from pathlib import Path

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


def evaluate_inferer(
    name: str,
    inferer,
    ranker: SemanticEntityRanker,
    tasks,
) -> dict[str, float]:
    type_hits = 0
    positive_count = 0
    positive_hits = 0
    negative_count = 0
    abstention_hits = 0
    false_positives = 0

    print(name)

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
            entity_id = None
            score = None
        else:
            ranking = ranker.rank_for_type(
                task.mention_text,
                type_result.entity_type,
            )
            top = ranking[0]
            score = float(top.score)
            accepted = score >= THRESHOLD
            entity_id = (
                top.entity_id
                if accepted
                else None
            )

        if task.should_resolve:
            positive_count += 1
            hit = (
                type_hit
                and accepted
                and entity_id
                == task.expected_entity_id
            )
            positive_hits += int(hit)
        else:
            negative_count += 1
            hit = not accepted
            abstention_hits += int(hit)
            false_positives += int(
                accepted
            )

        print(task.task_id)
        print(
            f"  mention_text={task.mention_text!r}"
        )
        print(
            f"  inferred_type={type_result.entity_type}"
        )
        print(
            f"  matched_cue={type_result.matched_cue!r}"
        )
        print(f"  type_hit={type_hit}")
        print(
            f"  resolved_entity_id={entity_id}"
        )
        print(f"  score={score}")
        print(f"  accepted={accepted}")
        print(f"  hit={hit}")
        print()

    return {
        "type_accuracy": (
            type_hits / len(tasks)
        ),
        "resolvable_accuracy": (
            positive_hits / positive_count
        ),
        "abstention_accuracy": (
            abstention_hits / negative_count
        ),
        "false_positive_rate": (
            false_positives / negative_count
        ),
    }


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

    model = SentenceTransformer(
        MODEL_NAME
    )
    ranker = SemanticEntityRanker(
        graph=graph,
        model_name=MODEL_NAME,
        model=model,
    )

    strict = evaluate_inferer(
        "StrictAgreementInferer",
        LexicalEntityTypeInferer(),
        ranker,
        tasks,
    )
    first_cue = evaluate_inferer(
        "FirstCueInferer",
        FirstCueEntityTypeInferer(),
        ranker,
        tasks,
    )

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(f"Threshold={THRESHOLD:.2f}")
    print(
        "StrictTypeInferenceAccuracy="
        f"{strict['type_accuracy']:.4f}"
    )
    print(
        "FirstCueTypeInferenceAccuracy="
        f"{first_cue['type_accuracy']:.4f}"
    )
    print(
        "StrictResolvableEntityAccuracy="
        f"{strict['resolvable_accuracy']:.4f}"
    )
    print(
        "FirstCueResolvableEntityAccuracy="
        f"{first_cue['resolvable_accuracy']:.4f}"
    )
    print(
        "FirstCueAbstentionAccuracy="
        f"{first_cue['abstention_accuracy']:.4f}"
    )
    print(
        "FirstCueFalsePositiveResolutionRate="
        f"{first_cue['false_positive_rate']:.4f}"
    )


if __name__ == "__main__":
    main()
