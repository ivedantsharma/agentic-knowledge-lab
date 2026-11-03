from pathlib import Path

from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)


TASK_PATH = Path(
    "data/processed/phase3_multihop_tasks_v4.json"
)


def test_phase3_multitask_benchmark_has_multiple_chain_shapes() -> None:
    tasks = load_multihop_tasks_json(TASK_PATH)

    assert len(tasks) >= 4
    assert {len(task.hops) for task in tasks} == {2, 3}
    assert len({task.task_id for task in tasks}) == len(tasks)
