"""EXP-124: source-level compatibility gate with evaluator-safe controls."""

import json
from pathlib import Path

import pytest

from scripts.run_phase13_policy_feasibility_audit import (
    DOCS,
    RL_SCRIPT,
    ROUTES,
    SFT_DATA,
    SFT_SCRIPT,
    audit_policy_feasibility,
    main,
)


def _copy(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    paths = (SFT_DATA, ROUTES, DOCS, SFT_SCRIPT, RL_SCRIPT)
    output = []
    for path in paths:
        destination = tmp_path / path.name
        destination.write_bytes(path.read_bytes())
        output.append(destination)
    return tuple(output)


def test_real_policy_contract_cannot_support_direct_sft_vs_rl_claim() -> None:
    audit = audit_policy_feasibility()
    assert audit.route_count == 12
    assert audit.shared_route_tasks == 12
    assert dict(audit.split_sizes) == {"train": 11, "dev": 3, "heldout": 3}
    assert "REFORMULATE" in audit.sft_actions
    assert "STOP" in audit.rl_actions
    assert "REFORMULATE" not in audit.rl_actions
    assert "STOP" not in audit.sft_actions
    assert not audit.identical_action_space
    assert not audit.shared_retriever
    assert not audit.shared_terminal_protocol
    assert not audit.same_heldout_split
    assert not audit.independent_new_families_present
    assert not audit.ready_for_direct_learned_comparison
    assert len(audit.hashes) == 5
    assert all(len(digest) == 64 for _, digest in audit.hashes)


def test_budget_label_comparison_only_counts_shared_tasks() -> None:
    audit = audit_policy_feasibility()
    assert (
        audit.budget_label_matches
        + audit.budget_label_mismatches
        + audit.budget_label_unmappable
        == audit.shared_route_tasks
    )
    assert audit.budget_label_mismatches > 0
    assert len(audit.sft_family_splits) == 6


def test_source_hashes_deterministic() -> None:
    assert audit_policy_feasibility() == audit_policy_feasibility()


def test_duplicate_sft_task_id_fails_closed(tmp_path: Path) -> None:
    sft, routes, docs, sft_script, rl_script = _copy(tmp_path)
    data = json.loads(sft.read_text(encoding="utf-8"))
    data[1]["source_task_id"] = data[0]["source_task_id"]
    sft.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate supervised task IDs"):
        audit_policy_feasibility(
            sft_path=sft, routes_path=routes, docs_path=docs,
            sft_script_path=sft_script, rl_script_path=rl_script,
        )


def test_split_leakage_fails_closed(tmp_path: Path) -> None:
    sft, routes, docs, sft_script, rl_script = _copy(tmp_path)
    data = json.loads(sft.read_text(encoding="utf-8"))
    data[0]["split"] = "train"
    sft.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="SFT family used"):
        audit_policy_feasibility(
            sft_path=sft, routes_path=routes, docs_path=docs,
            sft_script_path=sft_script, rl_script_path=rl_script,
        )


def test_unknown_sft_action_fails_closed(tmp_path: Path) -> None:
    sft, routes, docs, sft_script, rl_script = _copy(tmp_path)
    data = json.loads(sft.read_text(encoding="utf-8"))
    data[0]["target_action"] = "STOP"
    sft.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="unknown SFT action"):
        audit_policy_feasibility(
            sft_path=sft, routes_path=routes, docs_path=docs,
            sft_script_path=sft_script, rl_script_path=rl_script,
        )


def test_driver_labels_results_as_feasibility_only(capsys) -> None:
    main()
    out = capsys.readouterr().out
    assert "EXP-124 Gate A" in out
    assert "ready_for_direct_learned_comparison=False" in out
    assert "BLOCKED:" in out
    assert "No trained model inference" in out
