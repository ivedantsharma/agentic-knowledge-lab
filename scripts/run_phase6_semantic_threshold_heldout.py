import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
    ThresholdedSemanticEntityResolver,
)
from knowledgebench.tasks.graph_schema import (
    EntityMentionResolutionTask,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
THRESHOLD = 0.39

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_semantic_threshold_heldout_tasks_v0.json"
)


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        EntityMentionResolutionTask.model_validate(item)
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
    resolver = ThresholdedSemanticEntityResolver(
        ranker=ranker,
        threshold=THRESHOLD,
    )

    correct = 0
    positive_count = 0
    positive_hits = 0
    negative_count = 0
    abstention_hits = 0
    false_positive_count = 0

    for task in tasks:
        result = resolver.resolve(
            task.mention_text
        )

        if task.should_resolve:
            positive_count += 1
            hit = (
                result.accepted
                and result.entity_id
                == task.expected_entity_id
            )
            positive_hits += int(hit)
        else:
            negative_count += 1
            hit = not result.accepted
            abstention_hits += int(hit)
            false_positive_count += int(
                result.accepted
            )

        correct += int(hit)

        print(task.task_id)
        print(f"category={task.category}")
        print(f"mention_text={task.mention_text!r}")
        print(
            f"  resolved_entity_id={result.entity_id}"
        )
        print(f"  score={result.score:.6f}")
        print(
            f"  threshold={THRESHOLD:.2f}"
        )
        print(
            f"  accepted={result.accepted}"
        )
        print(
            f"  expected_entity_id={task.expected_entity_id}"
        )
        print(f"  hit={hit}")
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        f"Threshold={THRESHOLD:.2f}"
    )
    print(
        "OverallAccuracy="
        f"{correct / task_count:.4f}"
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
        f"{false_positive_count / negative_count:.4f}"
    )


if __name__ == "__main__":
    main()
