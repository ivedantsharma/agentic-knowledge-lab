import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

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
    "data/processed/phase6_typed_entity_heldout_tasks_v0.json"
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

    unconstrained_hits = 0
    typed_hits = 0
    positive_count = 0
    typed_abstention_hits = 0
    negative_count = 0
    typed_false_positives = 0

    for task in tasks:
        unrestricted = ranker.rank(
            task.mention_text
        )
        typed = ranker.rank_for_type(
            task.mention_text,
            task.expected_entity_type,
        )

        unrestricted_top = unrestricted[0]
        typed_top = typed[0]

        typed_accepted = typed_top.score >= THRESHOLD

        print(task.task_id)
        print(f"category={task.category}")
        print(f"mention_text={task.mention_text!r}")
        print(f"expected_entity_type={task.expected_entity_type}")
        print(
            "  unrestricted_top="
            f"{unrestricted_top.entity_id} "
            f"score={unrestricted_top.score:.6f}"
        )
        print(
            "  typed_top="
            f"{typed_top.entity_id} "
            f"score={typed_top.score:.6f}"
        )
        print(f"  typed_accepted={typed_accepted}")

        if task.should_resolve:
            positive_count += 1

            unrestricted_hit = (
                unrestricted_top.entity_id
                == task.expected_entity_id
                and unrestricted_top.score >= THRESHOLD
            )
            typed_hit = (
                typed_accepted
                and typed_top.entity_id
                == task.expected_entity_id
            )

            unconstrained_hits += int(unrestricted_hit)
            typed_hits += int(typed_hit)

            print(f"  unrestricted_hit={unrestricted_hit}")
            print(f"  typed_hit={typed_hit}")
        else:
            negative_count += 1

            typed_abstention = not typed_accepted
            typed_abstention_hits += int(typed_abstention)
            typed_false_positives += int(typed_accepted)

            print(f"  typed_abstention={typed_abstention}")

        print()

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(f"Threshold={THRESHOLD:.2f}")
    print(
        "UnconstrainedResolvableAccuracy="
        f"{unconstrained_hits / positive_count:.4f}"
    )
    print(
        "TypedResolvableAccuracy="
        f"{typed_hits / positive_count:.4f}"
    )
    print(
        "TypedAbstentionAccuracy="
        f"{typed_abstention_hits / negative_count:.4f}"
    )
    print(
        "TypedFalsePositiveResolutionRate="
        f"{typed_false_positives / negative_count:.4f}"
    )


if __name__ == "__main__":
    main()
