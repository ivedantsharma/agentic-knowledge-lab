import json
from pathlib import Path

from knowledgebench.tasks.multihop_schema import MultiHopTask


def load_multihop_tasks_json(
    path: str | Path,
) -> list[MultiHopTask]:
    """Load multi-hop tasks from a JSON array."""
    payload = json.loads(
        Path(path).read_text(encoding="utf-8")
    )

    return [
        MultiHopTask.model_validate(item)
        for item in payload
    ]
