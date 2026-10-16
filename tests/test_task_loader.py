import json

import pytest

from knowledgebench.tasks.loader import DatasetLoadError, load_tasks_jsonl


def test_load_tasks_jsonl(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "task_id": "kb-001",
                        "question": "What is BM25?",
                        "relevant_document_ids": ["doc_bm25"],
                        "category": "direct",
                    }
                ),
                json.dumps(
                    {
                        "task_id": "kb-002",
                        "question": "What is dense retrieval?",
                        "relevant_document_ids": ["doc_dense"],
                        "category": "direct",
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    tasks = load_tasks_jsonl(path)

    assert len(tasks) == 2
    assert tasks[0].task_id == "kb-001"
    assert tasks[0].relevant_document_ids == {"doc_bm25"}


def test_blank_lines_are_ignored(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        '\n{"task_id":"kb-001","question":"Q","category":"direct"}\n\n',
        encoding="utf-8",
    )

    tasks = load_tasks_jsonl(path)

    assert len(tasks) == 1


def test_invalid_json_reports_line_number(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        '{"task_id":"kb-001","question":"Q","category":"direct"}\n{bad json}\n',
        encoding="utf-8",
    )

    with pytest.raises(DatasetLoadError, match="line 2"):
        load_tasks_jsonl(path)


def test_invalid_task_reports_line_number(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        '{"task_id":"   ","question":"Q","category":"direct"}\n',
        encoding="utf-8",
    )

    with pytest.raises(DatasetLoadError, match="line 1"):
        load_tasks_jsonl(path)


def test_duplicate_task_id_is_rejected(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        "\n".join(
            [
                '{"task_id":"kb-001","question":"Q1","category":"direct"}',
                '{"task_id":"kb-001","question":"Q2","category":"direct"}',
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(DatasetLoadError, match="Duplicate task_id"):
        load_tasks_jsonl(path)
