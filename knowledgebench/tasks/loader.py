import json
from pathlib import Path

from pydantic import ValidationError

from knowledgebench.tasks.schema import KnowledgeTask


class DatasetLoadError(ValueError):
    """Raised when a KnowledgeBench dataset cannot be loaded safely."""


def load_tasks_jsonl(path: str | Path) -> list[KnowledgeTask]:
    """Load and validate KnowledgeBench tasks from a JSONL file."""
    dataset_path = Path(path)
    tasks: list[KnowledgeTask] = []
    seen_task_ids: set[str] = set()

    with dataset_path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line:
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise DatasetLoadError(
                    f"Invalid JSON on line {line_number}: {exc.msg}"
                ) from exc

            try:
                task = KnowledgeTask.model_validate(payload)
            except ValidationError as exc:
                raise DatasetLoadError(
                    f"Invalid KnowledgeTask on line {line_number}: {exc}"
                ) from exc

            if task.task_id in seen_task_ids:
                raise DatasetLoadError(
                    f"Duplicate task_id '{task.task_id}' on line {line_number}"
                )

            seen_task_ids.add(task.task_id)
            tasks.append(task)

    return tasks
