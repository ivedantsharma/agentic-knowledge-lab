import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.graph.path_search import GraphPathEnumerator, SemanticGraphPathRanker
from knowledge_engine.graph.schema import ClaimGraph
from knowledgebench.tasks.graph_schema import GraphTraversalTask


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GRAPH_PATH = Path(
    "data/processed/phase6_branching_claim_graph_v0.json"
)
TASK_PATH = Path(
    "data/processed/phase6_graph_tasks_v0.json"
)


def main() -> None:
    graph = ClaimGraph.model_validate_json(
        GRAPH_PATH.read_text(encoding="utf-8")
    )
    tasks = [
        GraphTraversalTask.model_validate(item)
        for item in json.loads(
            TASK_PATH.read_text(encoding="utf-8")
        )
    ]

    model = SentenceTransformer(MODEL_NAME)
    enumerator = GraphPathEnumerator(graph)
    ranker = SemanticGraphPathRanker(
        model_name=MODEL_NAME,
        model=model,
    )

    path_hits = 0
    answer_hits = 0
    total_candidates = 0

    for task in tasks:
        candidates = enumerator.enumerate_literal_paths(
            start_entity_id=task.start_entity_id,
            max_hops=3,
        )
        ranking = ranker.rank(
            task.question,
            candidates,
        )

        total_candidates += len(candidates)
        top = ranking[0]

        path_hit = (
            top.candidate.claim_ids
            == task.expected_claim_ids
        )
        answer_hit = (
            top.candidate.final_value.casefold()
            == task.expected_answer.casefold()
        )

        path_hits += int(path_hit)
        answer_hits += int(answer_hit)

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  start_entity_id={task.start_entity_id}"
        )
        print(
            f"  candidate_paths={len(candidates)}"
        )

        for rank, item in enumerate(
            ranking,
            start=1,
        ):
            marker = (
                " CORRECT"
                if item.candidate.claim_ids
                == task.expected_claim_ids
                else ""
            )
            print(
                f"  rank={rank} "
                f"score={item.score:.6f} "
                f"relations={item.candidate.relation_path} "
                f"answer={item.candidate.final_value!r}"
                f"{marker}"
            )

        print(f"  path_hit={path_hit}")
        print(f"  answer_hit={answer_hit}")
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "PathSelectionAccuracy="
        f"{path_hits / task_count:.4f}"
    )
    print(
        "AnswerAccuracy="
        f"{answer_hits / task_count:.4f}"
    )
    print(
        "AvgCandidatePaths="
        f"{total_candidates / task_count:.2f}"
    )


if __name__ == "__main__":
    main()
