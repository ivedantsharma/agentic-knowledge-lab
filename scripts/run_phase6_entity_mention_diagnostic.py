import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
)
from knowledgebench.tasks.graph_schema import (
    EntityMentionResolutionTask,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_entity_mention_diagnostic_tasks_v0.json"
)


def rank_of(
    ranking,
    entity_id: str,
) -> int:
    return next(
        rank
        for rank, candidate in enumerate(
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
        EntityMentionResolutionTask.model_validate(item)
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

    positive_count = 0
    whole_hit_1 = 0
    mention_hit_1 = 0
    mention_hit_3 = 0

    positive_mention_top_scores = []
    negative_mention_top_scores = []

    for task in tasks:
        whole_ranking = ranker.rank(
            task.question
        )
        mention_ranking = ranker.rank(
            task.mention_text
        )

        print(task.task_id)
        print(f"category={task.category}")
        print(f"question={task.question}")
        print(
            f"mention_text={task.mention_text!r}"
        )

        print("  whole_question_top3:")
        for rank, candidate in enumerate(
            whole_ranking[:3],
            start=1,
        ):
            print(
                f"    rank={rank} "
                f"entity={candidate.entity_id} "
                f"score={candidate.score:.6f}"
            )

        print("  mention_top3:")
        for rank, candidate in enumerate(
            mention_ranking[:3],
            start=1,
        ):
            marker = ""
            if (
                task.expected_entity_id
                == candidate.entity_id
            ):
                marker = " CORRECT"

            print(
                f"    rank={rank} "
                f"entity={candidate.entity_id} "
                f"score={candidate.score:.6f}"
                f"{marker}"
            )

        if task.should_resolve:
            positive_count += 1

            whole_gold_rank = rank_of(
                whole_ranking,
                task.expected_entity_id,
            )
            mention_gold_rank = rank_of(
                mention_ranking,
                task.expected_entity_id,
            )

            whole_hit_1 += int(
                whole_gold_rank == 1
            )
            mention_hit_1 += int(
                mention_gold_rank == 1
            )
            mention_hit_3 += int(
                mention_gold_rank <= 3
            )

            positive_mention_top_scores.append(
                float(mention_ranking[0].score)
            )

            print(
                f"  whole_gold_rank={whole_gold_rank}"
            )
            print(
                f"  mention_gold_rank={mention_gold_rank}"
            )
        else:
            negative_mention_top_scores.append(
                float(mention_ranking[0].score)
            )
            print(
                "  expected_behavior=ABSTAIN"
            )

        print()

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(
        "WholeQuestionHit@1="
        f"{whole_hit_1 / positive_count:.4f}"
    )
    print(
        "MentionSpanHit@1="
        f"{mention_hit_1 / positive_count:.4f}"
    )
    print(
        "MentionSpanHit@3="
        f"{mention_hit_3 / positive_count:.4f}"
    )
    print(
        "PositiveMentionTopScores="
        f"{[round(score, 6) for score in positive_mention_top_scores]}"
    )
    print(
        "NegativeMentionTopScores="
        f"{[round(score, 6) for score in negative_mention_top_scores]}"
    )


if __name__ == "__main__":
    main()
