from pathlib import Path

from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)

TASK_PATH = Path(
    "data/processed/phase4_planner_benchmark_v0.json"
)


def test_phase4_planner_benchmark_contains_known_and_ood_tasks() -> None:
    tasks = load_multihop_tasks_json(
        TASK_PATH
    )

    assert len(tasks) == 5
    assert {task.task_id for task in tasks} == {
        "mh-001",
        "mh-002",
        "mh-003",
        "mh-004",
        "ood-001",
    }

    assert any(
        task.category == "unseen_dead_letter_intent"
        for task in tasks
    )

    assert {len(task.hops) for task in tasks} == {2, 3}
