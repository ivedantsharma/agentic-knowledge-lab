"""EXP-122 Gate B verifies exact provenance parity and path integrity."""

import json
from pathlib import Path

import pytest

from knowledgebench.datasets.representation_bridge import (
    DEFAULT_GRAPH,
    DEFAULT_TASKS,
    build_common_substrate,
)
from scripts.run_phase13_common_representation_contract import main


def _copy(tmp_path: Path) -> tuple[Path, Path]:
    graph = tmp_path / "graph.json"
    tasks = tmp_path / "tasks.json"
    graph.write_bytes(DEFAULT_GRAPH.read_bytes())
    tasks.write_bytes(DEFAULT_TASKS.read_bytes())
    return graph, tasks


def _edit(path: Path, mutate) -> None:
    raw = json.loads(path.read_text(encoding="utf-8"))
    mutate(raw)
    path.write_text(json.dumps(raw), encoding="utf-8")


def test_real_graph_creates_one_evidence_atom_per_original_reference() -> None:
    substrate = build_common_substrate()
    assert len(substrate.graph.claims) == 15
    assert len(substrate.tasks) == 4
    expected = [
        (claim.claim_id, evidence.document_id, evidence.evidence_text)
        for claim in substrate.graph.claims
        for evidence in claim.evidence
    ]
    actual = [
        (atom.claim_id, atom.document_id, atom.evidence_text)
        for atom in substrate.atoms
    ]
    assert actual == expected


def test_flat_and_hierarchy_preserve_exact_evidence_and_provenance() -> None:
    substrate = build_common_substrate()
    sections = [
        section
        for document in substrate.hierarchy
        for section in document.sections
    ]
    sections_by_id = {
        section.metadata["atom_id"]: section for section in sections
    }
    assert len(sections_by_id) == len(substrate.atoms)
    flat = dict(substrate.flat_corpus())
    for atom in substrate.atoms:
        section = sections_by_id[atom.atom_id]
        assert section.text == atom.evidence_text
        assert section.title == atom.relation
        assert section.metadata["claim_id"] == atom.claim_id
        assert section.metadata["source_document_id"] == atom.document_id
        assert flat[atom.atom_id] == f"Relation: {atom.relation}. {atom.evidence_text}"


def test_no_task_gold_inserted_into_representation_metadata() -> None:
    substrate = build_common_substrate()
    for doc in substrate.hierarchy:
        assert "expected_answer" not in doc.metadata
        assert "expected_claim_ids" not in doc.metadata
        for section in doc.sections:
            assert "expected_answer" not in section.metadata
            assert "expected_claim_ids" not in section.metadata


def test_graph_task_path_from_source_is_consistent() -> None:
    substrate = build_common_substrate()
    claims = {claim.claim_id: claim for claim in substrate.graph.claims}
    for task in substrate.tasks:
        current = task.start_entity_id
        for claim_id in task.expected_claim_ids:
            claim = claims[claim_id]
            assert claim.subject_entity_id == current
            current = claim.object_entity_id
        assert claims[task.expected_claim_ids[-1]].object_value == task.expected_answer


def test_missing_expected_claim_rejected(tmp_path: Path) -> None:
    graph, tasks = _copy(tmp_path)
    _edit(tasks, lambda x: x[0].update(expected_claim_ids=["unknown"]))
    with pytest.raises(ValueError, match="missing claim"):
        build_common_substrate(graph, tasks)


def test_wrong_expected_answer_rejected(tmp_path: Path) -> None:
    graph, tasks = _copy(tmp_path)
    _edit(tasks, lambda x: x[0].update(expected_answer="fake answer"))
    with pytest.raises(ValueError, match="expected answer disagrees"):
        build_common_substrate(graph, tasks)


def test_broken_relation_chain_rejected(tmp_path: Path) -> None:
    graph, tasks = _copy(tmp_path)
    _edit(tasks, lambda x: x[0]["relation_path"].__setitem__(0, "wrong"))
    with pytest.raises(ValueError, match="continuity/relation mismatch"):
        build_common_substrate(graph, tasks)


def test_extra_evidence_reference_is_preserved(tmp_path: Path) -> None:
    graph, tasks = _copy(tmp_path)

    def add_reference(x) -> None:
        x["claims"][0]["evidence"].append(
            {"document_id": "source-extra", "evidence_text": "New independent source."}
        )

    _edit(graph, add_reference)
    substrate = build_common_substrate(graph, tasks)
    assert len(substrate.atoms) == sum(
        len(claim.evidence) for claim in substrate.graph.claims
    )
    assert any(atom.document_id == "source-extra" for atom in substrate.atoms)


def test_gate_b_contract_driver(capsys) -> None:
    main()
    out = capsys.readouterr().out
    assert "EXP-122 Gate B" in out
    assert "PASS: Every source claim evidence span appears once" in out
    assert "NO retriever scores" in out
    assert "graph_tasks=4" in out
