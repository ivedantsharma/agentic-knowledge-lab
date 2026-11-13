"""EXP-122 Gate A validates existing Phase 5/6 source provenance."""

import json
from pathlib import Path

import pytest

from scripts.run_phase13_representation_substrate_audit import (
    GRAPH_SOURCE,
    GRAPH_TASKS,
    HIERARCHY_DOCS,
    HIERARCHY_TASKS,
    audit_substrates,
    main,
)


def copies(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    result = []
    for original in (HIERARCHY_DOCS, HIERARCHY_TASKS, GRAPH_SOURCE, GRAPH_TASKS):
        target = tmp_path / original.name
        target.write_bytes(original.read_bytes())
        result.append(target)
    return tuple(result)


def update_json(path: Path, transform) -> None:
    rows = json.loads(path.read_text(encoding="utf-8"))
    transform(rows)
    path.write_text(json.dumps(rows), encoding="utf-8")


def test_current_substrates_have_no_exact_paired_task_crosswalk() -> None:
    result = audit_substrates()
    assert result.hierarchy_documents == 6
    assert result.hierarchy_tasks == 3
    assert result.graph_tasks == 4
    assert result.graph_claims > 0
    assert result.graph_entities > 0
    assert not result.complete_paired_task_crosswalk
    assert result.shared_task_ids == ()
    assert result.shared_exact_questions == ()
    assert all(len(digest) == 64 for _, digest in result.hashes)


def test_substrate_inventory_is_deterministic() -> None:
    assert audit_substrates() == audit_substrates()


def test_missing_hierarchy_source_rejected(tmp_path: Path) -> None:
    docs, tasks, graph, graph_tasks = copies(tmp_path)
    update_json(tasks, lambda rows: rows[0].update(source_document_id="absent"))
    with pytest.raises(ValueError, match="hierarchy evidence source"):
        audit_substrates(docs, tasks, graph, graph_tasks)


def test_missing_graph_claim_rejected(tmp_path: Path) -> None:
    docs, tasks, graph, graph_tasks = copies(tmp_path)
    update_json(graph_tasks, lambda rows: rows[0].update(expected_claim_ids=["absent"]))
    with pytest.raises(ValueError, match="graph expected claim"):
        audit_substrates(docs, tasks, graph, graph_tasks)


def test_duplicate_entity_id_rejected(tmp_path: Path) -> None:
    docs, tasks, graph, graph_tasks = copies(tmp_path)
    update_json(
        graph,
        lambda payload: payload["entities"][1].update(
            entity_id=payload["entities"][0]["entity_id"]
        ),
    )
    with pytest.raises(ValueError, match="duplicate entity_id"):
        audit_substrates(docs, tasks, graph, graph_tasks)


def test_malformed_source_schema_rejected(tmp_path: Path) -> None:
    docs, tasks, graph, graph_tasks = copies(tmp_path)
    graph.write_text('["unexpected", "list"]', encoding="utf-8")
    with pytest.raises(TypeError, match="unexpected shapes"):
        audit_substrates(docs, tasks, graph, graph_tasks)


def test_experiment_driver_outputs_no_performance_claim(capsys) -> None:
    main()
    output = capsys.readouterr().out
    assert "EXP-122 Gate A" in output
    assert "complete_paired_task_crosswalk=False" in output
    assert "BLOCKED:" in output
    assert "NO architecture scores computed" in output
    assert output.count("SHA256 ") == 4
