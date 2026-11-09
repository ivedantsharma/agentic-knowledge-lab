import json
from pathlib import Path

from knowledgebench.tasks.graph_schema import (
    SemanticEntityMentionTask,
)

TASK_PATH = Path(
    "data/processed/phase6_semantic_entity_mentions_v0.json"
)


def test_semantic_mention_tasks_validate() -> None:
    payload = json.loads(
        TASK_PATH.read_text(encoding="utf-8")
    )

    tasks = [
        SemanticEntityMentionTask.model_validate(item)
        for item in payload
    ]

    assert len(tasks) == 2
    assert (
        tasks[1].mention_text
        == "infrastructure reliability group"
    )
