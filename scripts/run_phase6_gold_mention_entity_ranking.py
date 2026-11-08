import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
)
from knowledgebench.tasks.graph_schema import (
    SemanticEntityMentionTask,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_semantic_entity_mentions_v0.json"
)


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )

    tasks = [
        SemanticEntityMentionTask.model_validate(item)
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

    full_question_hits = 0
    mention_hits = 0

    for task in tasks:
        full_ranking = ranker.rank(
            task.question
        )
        mention_ranking = ranker.rank(
            task.mention_text
        )

        full_gold_rank = next(
            rank
            for rank, candidate in enumerate(
                full_ranking,
                start=1,
            )
            if candidate.entity_id
            == task.expected_entity_id
        )

        mention_gold_rank = next(
            rank
            for rank, candidate in enumerate(
                mention_ranking,
                start=1,
            )
            if candidate.entity_id
            == task.expected_entity_id
        )

        full_question_hits += int(
            full_gold_rank == 1
        )
        mention_hits += int(
            mention_gold_rank == 1
        )

        print(task.task_id)
        print(f"category={task.category}")
        print(f"question={task.question}")
        print(
            f"mention_text={task.mention_text!r}"
        )
        print(
            "  full_question_top1="
            f"{full_ranking[0].entity_id} "
            f"score={full_ranking[0].score:.6f}"
        )
        print(
            f"  full_question_gold_rank={full_gold_rank}"
        )
        print(
            "  mention_top1="
            f"{mention_ranking[0].entity_id} "
            f"score={mention_ranking[0].score:.6f}"
        )
        print(
            f"  mention_gold_rank={mention_gold_rank}"
        )

        print("  mention_top3:")
        for rank, candidate in enumerate(
            mention_ranking[:3],
            start=1,
        ):
            marker = (
                " CORRECT"
                if candidate.entity_id
                == task.expected_entity_id
                else ""
            )
            print(
                f"    rank={rank} "
                f"entity={candidate.entity_id} "
                f"score={candidate.score:.6f}"
                f"{marker}"
            )

        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "FullQuestionHit@1="
        f"{full_question_hits / task_count:.4f}"
    )
    print(
        "GoldMentionHit@1="
        f"{mention_hits / task_count:.4f}"
    )


if __name__ == "__main__":
    main()
