import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.entity_resolution import (
    LexicalEntityResolver,
)
from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.graph.semantic_entity_resolution import (
    SemanticEntityRanker,
)
from knowledgebench.tasks.graph_schema import EntityResolutionTask

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GRAPH_PATH = Path(
    "data/processed/phase6_claim_graph_entity_stress_v1.json"
)
TASK_PATH = Path(
    "data/processed/phase6_semantic_entity_diagnostic_tasks_v0.json"
)


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        EntityResolutionTask.model_validate(item)
        for item in json.loads(
            TASK_PATH.read_text(encoding="utf-8")
        )
    ]

    model = SentenceTransformer(
        MODEL_NAME
    )
    lexical = LexicalEntityResolver(graph)
    semantic = SemanticEntityRanker(
        graph=graph,
        model_name=MODEL_NAME,
        model=model,
    )

    resolvable_count = 0
    semantic_hit_at_1 = 0
    semantic_hit_at_3 = 0
    lexical_abstentions = 0

    positive_top_scores = []
    negative_top_scores = []

    for task in tasks:
        print(task.task_id)
        print(f"category={task.category}")
        print(f"question={task.question}")

        try:
            lexical_result = lexical.resolve(
                task.question
            )
            print(
                "  lexical_result="
                f"{lexical_result.entity_id}"
            )
        except ValueError:
            lexical_abstentions += 1
            print("  lexical_result=ABSTAIN")

        ranking = semantic.rank(
            task.question
        )

        for rank, candidate in enumerate(
            ranking[:5],
            start=1,
        ):
            marker = ""
            if (
                task.expected_entity_id
                == candidate.entity_id
            ):
                marker = " CORRECT"

            print(
                f"  rank={rank} "
                f"entity={candidate.entity_id} "
                f"score={candidate.score:.6f}"
                f"{marker}"
            )

        top_score = ranking[0].score

        if task.should_resolve:
            resolvable_count += 1

            gold_rank = next(
                rank
                for rank, candidate in enumerate(
                    ranking,
                    start=1,
                )
                if candidate.entity_id
                == task.expected_entity_id
            )

            semantic_hit_at_1 += int(
                gold_rank == 1
            )
            semantic_hit_at_3 += int(
                gold_rank <= 3
            )
            positive_top_scores.append(
                top_score
            )

            print(
                f"  gold_rank={gold_rank}"
            )
        else:
            negative_top_scores.append(
                top_score
            )
            print(
                "  expected_behavior=ABSTAIN"
            )

        print()

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(
        "LexicalAbstentionRate="
        f"{lexical_abstentions / len(tasks):.4f}"
    )
    print(
        "SemanticHit@1="
        f"{semantic_hit_at_1 / resolvable_count:.4f}"
    )
    print(
        "SemanticHit@3="
        f"{semantic_hit_at_3 / resolvable_count:.4f}"
    )
    print(
        "PositiveTopScores="
        f"{[round(score, 6) for score in positive_top_scores]}"
    )
    print(
        "NegativeTopScores="
        f"{[round(score, 6) for score in negative_top_scores]}"
    )


if __name__ == "__main__":
    main()
