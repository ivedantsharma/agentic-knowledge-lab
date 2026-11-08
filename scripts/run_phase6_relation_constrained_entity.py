import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
)
from knowledgebench.tasks.graph_schema import (
    RelationConstrainedEntityTask,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_relation_constrained_entity_tasks_v0.json"
)


def rank_of(
    entity_id: str,
    ranking,
) -> int:
    return next(
        index
        for index, candidate in enumerate(
            ranking,
            start=1,
        )
        if candidate.entity_id == entity_id
    )


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        RelationConstrainedEntityTask.model_validate(item)
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

    constrained_hits = 0
    total_unconstrained_candidates = 0
    total_constrained_candidates = 0

    for task in tasks:
        unconstrained = ranker.rank(
            task.question
        )
        constrained = ranker.rank_for_relation(
            task.question,
            task.first_relation,
        )

        unconstrained_gold_rank = rank_of(
            task.expected_entity_id,
            unconstrained,
        )
        constrained_gold_rank = rank_of(
            task.expected_entity_id,
            constrained,
        )

        constrained_hit = (
            constrained_gold_rank == 1
        )
        constrained_hits += int(
            constrained_hit
        )

        total_unconstrained_candidates += len(
            unconstrained
        )
        total_constrained_candidates += len(
            constrained
        )

        print(task.task_id)
        print(f"category={task.category}")
        print(f"question={task.question}")
        print(
            f"  first_relation={task.first_relation}"
        )
        print(
            f"  unconstrained_gold_rank={unconstrained_gold_rank}"
        )
        print(
            "  unconstrained_top="
            f"{unconstrained[0].entity_id} "
            f"score={unconstrained[0].score:.6f}"
        )
        print(
            f"  valid_subjects="
            f"{sorted(ranker.valid_subjects_for_relation(task.first_relation))}"
        )
        print(
            f"  constrained_gold_rank={constrained_gold_rank}"
        )
        print(
            "  constrained_top="
            f"{constrained[0].entity_id} "
            f"score={constrained[0].score:.6f}"
        )
        print(
            f"  constrained_hit={constrained_hit}"
        )
        print()

    task_count = len(tasks)

    avg_unconstrained = (
        total_unconstrained_candidates
        / task_count
    )
    avg_constrained = (
        total_constrained_candidates
        / task_count
    )

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "ConstrainedHit@1="
        f"{constrained_hits / task_count:.4f}"
    )
    print(
        "AvgUnconstrainedCandidates="
        f"{avg_unconstrained:.2f}"
    )
    print(
        "AvgConstrainedCandidates="
        f"{avg_constrained:.2f}"
    )
    print(
        "CandidateReduction="
        f"{1.0 - (avg_constrained / avg_unconstrained):.4f}"
    )


if __name__ == "__main__":
    main()
