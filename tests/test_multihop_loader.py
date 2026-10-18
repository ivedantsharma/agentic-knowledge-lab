import json

from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)


def test_load_multihop_tasks_json(tmp_path) -> None:
    path = tmp_path / "tasks.json"

    path.write_text(
        json.dumps(
            [
                {
                    "task_id": "mh-001",
                    "question": "Question?",
                    "expected_answer": "Answer",
                    "hops": [
                        {
                            "hop_index": 0,
                            "query": "First search",
                            "expected_document_id": "doc-1",
                            "expected_fact": "Fact 1",
                        }
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )

    tasks = load_multihop_tasks_json(path)

    assert len(tasks) == 1
    assert tasks[0].task_id == "mh-001"
    assert tasks[0].hops[0].expected_document_id == "doc-1"
