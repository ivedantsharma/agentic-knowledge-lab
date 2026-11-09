import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.entity_type import (
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
    type_inferer = LexicalEntityTypeInferer()

    type_hits = 0
    positive_count = 0
    positive_hits = 0
    negative_count = 0
    abstention_hits = 0
    false_positives = 0

    for task in tasks:
        type_result = type_inferer.infer(
            task.mention_text
        )

        print(task.task_id)
        print(f"category={task.category}")
        print(
            f"mention_text={task.mention_text!r}"
        )
        print(
            f"  inferred_type={type_result.entity_type}"
        )
        print(
            f"  matched_cue={type_result.matched_cue!r}"
        )

        type_hit = (
            type_result.entity_type
            == task.expected_entity_type
        )
        type_hits += int(type_hit)
        print(f"  type_hit={type_hit}")

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

        print(
            f"  resolved_entity_id={entity_id}"
        )
        print(f"  score={score}")
        print(f"  accepted={accepted}")

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

        print(f"  hit={hit}")
        print()

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(
        "TypeInferenceAccuracy="
        f"{type_hits / len(tasks):.4f}"
    )
    print(
        "ResolvableEntityAccuracy="
        f"{positive_hits / positive_count:.4f}"
    )
    print(
        "AbstentionAccuracy="
        f"{abstention_hits / negative_count:.4f}"
    )
    print(
        "FalsePositiveResolutionRate="
        f"{false_positives / negative_count:.4f}"
    )


if __name__ == "__main__":
    main()
