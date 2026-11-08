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


def resolve_with_type(
    ranker: SemanticEntityRanker,
    mention_text: str,
    entity_type: str | None,
) -> tuple[str | None, float | None, bool]:
    if entity_type is None:
        return None, None, False

    ranking = ranker.rank_for_type(
        mention_text,
        entity_type,
    )
    top = ranking[0]
    score = float(top.score)
    accepted = score >= THRESHOLD

    return (
        top.entity_id if accepted else None,
        score,
        accepted,
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

    original_inferer = LexicalEntityTypeInferer()
    first_cue_inferer = FirstCueEntityTypeInferer()

    original_type_hits = 0
    first_cue_type_hits = 0
    original_positive_hits = 0
    first_cue_positive_hits = 0
    positive_count = 0
    first_cue_abstention_hits = 0
    negative_count = 0
    first_cue_false_positives = 0

    for task in tasks:
        original_type = original_inferer.infer(
            task.mention_text
        )
        first_cue_type = first_cue_inferer.infer(
            task.mention_text
        )

        original_type_hit = (
            original_type.entity_type
            == task.expected_entity_type
        )
        first_cue_type_hit = (
            first_cue_type.entity_type
            == task.expected_entity_type
        )

        original_type_hits += int(
            original_type_hit
        )
        first_cue_type_hits += int(
            first_cue_type_hit
        )

        original_entity, original_score, original_accepted = (
            resolve_with_type(
                ranker,
                task.mention_text,
                original_type.entity_type,
            )
        )
        first_entity, first_score, first_accepted = (
            resolve_with_type(
                ranker,
                task.mention_text,
                first_cue_type.entity_type,
            )
        )

        print(task.task_id)
        print(f"category={task.category}")
        print(
            f"mention_text={task.mention_text!r}"
        )
        print(
            "  original_type="
            f"{original_type.entity_type} "
            f"cue={original_type.matched_cue!r}"
        )
        print(
            "  first_cue_type="
            f"{first_cue_type.entity_type} "
            f"cue={first_cue_type.matched_cue!r}"
        )
        print(
            "  original_resolution="
            f"{original_entity} "
            f"score={original_score} "
            f"accepted={original_accepted}"
        )
        print(
            "  first_cue_resolution="
            f"{first_entity} "
            f"score={first_score} "
            f"accepted={first_accepted}"
        )

        if task.should_resolve:
            positive_count += 1

            original_hit = (
                original_type_hit
                and original_accepted
                and original_entity
                == task.expected_entity_id
            )
            first_cue_hit = (
                first_cue_type_hit
                and first_accepted
                and first_entity
                == task.expected_entity_id
            )

            original_positive_hits += int(
                original_hit
            )
            first_cue_positive_hits += int(
                first_cue_hit
            )

            print(
                f"  original_hit={original_hit}"
            )
            print(
                f"  first_cue_hit={first_cue_hit}"
            )
        else:
            negative_count += 1

            first_cue_abstention = (
                not first_accepted
            )
            first_cue_abstention_hits += int(
                first_cue_abstention
            )
            first_cue_false_positives += int(
                first_accepted
            )

            print(
                "  first_cue_abstention="
                f"{first_cue_abstention}"
            )

        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "OriginalTypeInferenceAccuracy="
        f"{original_type_hits / task_count:.4f}"
    )
    print(
        "FirstCueTypeInferenceAccuracy="
        f"{first_cue_type_hits / task_count:.4f}"
    )
    print(
        "OriginalResolvableEntityAccuracy="
        f"{original_positive_hits / positive_count:.4f}"
    )
    print(
        "FirstCueResolvableEntityAccuracy="
        f"{first_cue_positive_hits / positive_count:.4f}"
    )
    print(
        "FirstCueAbstentionAccuracy="
        f"{first_cue_abstention_hits / negative_count:.4f}"
    )
    print(
        "FirstCueFalsePositiveResolutionRate="
        f"{first_cue_false_positives / negative_count:.4f}"
    )


if __name__ == "__main__":
    main()
