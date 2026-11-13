"""EXP-120: verify reproducible source inventory and leakage checks."""

import hashlib
import json
from pathlib import Path

import pytest

from scripts.run_phase13_campaign_inventory import (
    DOCS,
    POLICIES,
    ROUTES,
    build_inventory,
    main,
)


def _copies(tmp_path: Path) -> tuple[Path, Path, Path]:
    paths = []
    for source in (DOCS, ROUTES, POLICIES):
        target = tmp_path / source.name
        target.write_bytes(source.read_bytes())
        paths.append(target)
    return tuple(paths)


def _modify(path: Path, change) -> None:
    rows = json.loads(path.read_text(encoding="utf-8"))
    change(rows)
    path.write_text(json.dumps(rows), encoding="utf-8")


def test_current_inputs_have_expected_counts_and_families() -> None:
    inventory = build_inventory()
    assert inventory.document_count == 22
    assert inventory.route_count == 12
    assert inventory.policy_example_count == 17
    assert len(inventory.route_families) == 6
    assert sum(count for _, count in inventory.route_family_counts) == 12
    assert len(inventory.previously_inspected_families) == 5


def test_hashes_are_exact_file_bytes_and_stable() -> None:
    one = build_inventory()
    two = build_inventory()
    assert one == two
    for name, digest in one.file_hashes:
        assert len(digest) == 64
        assert digest == hashlib.sha256(Path(name).read_bytes()).hexdigest()


def test_route_family_sft_split_is_not_phase12_holdout() -> None:
    mapping = dict(build_inventory().route_sft_split_by_family)
    assert mapping["cirrus_retry"] == "train"
    assert mapping["meridian_rotation"] == "heldout"
    assert mapping["borealis_backup"] == "dev"
    assert mapping["solstice_cache"] == "train"
    assert mapping["nimbus_session"] == "train"
    assert mapping["orion_logs"] == "train"


def test_document_gold_must_exist(tmp_path: Path) -> None:
    docs, routes, policies = _copies(tmp_path)
    _modify(routes, lambda rows: rows[0].update(supporting_document_ids=["missing"]))
    with pytest.raises(ValueError, match="supporting documents"):
        build_inventory(docs, routes, policies)


def test_duplicate_source_task_id_rejected(tmp_path: Path) -> None:
    docs, routes, policies = _copies(tmp_path)
    _modify(
        policies,
        lambda rows: rows[1].update(source_task_id=rows[0]["source_task_id"]),
    )
    with pytest.raises(ValueError, match="duplicate source_task_id"):
        build_inventory(docs, routes, policies)


def test_duplicate_route_id_rejected(tmp_path: Path) -> None:
    docs, routes, policies = _copies(tmp_path)
    _modify(routes, lambda rows: rows[1].update(task_id=rows[0]["task_id"]))
    with pytest.raises(ValueError, match="duplicate task_id"):
        build_inventory(docs, routes, policies)


def test_question_join_mismatch_rejected(tmp_path: Path) -> None:
    docs, routes, policies = _copies(tmp_path)
    _modify(
        policies,
        lambda rows: next(
            row for row in rows if row["source_task_id"] == "route-003"
        ).update(question="inconsistent question"),
    )
    with pytest.raises(ValueError, match="source question mismatch"):
        build_inventory(docs, routes, policies)


def test_family_split_leakage_rejected(tmp_path: Path) -> None:
    docs, routes, policies = _copies(tmp_path)
    _modify(
        policies,
        lambda rows: next(
            row for row in rows if row["source_task_id"] == "route-004"
        ).update(split="dev"),
    )
    with pytest.raises(ValueError, match="split across"):
        build_inventory(docs, routes, policies)


def test_invalid_json_shape_rejected(tmp_path: Path) -> None:
    docs, routes, policies = _copies(tmp_path)
    docs.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(TypeError, match="top-level JSON list"):
        build_inventory(docs, routes, policies)


def test_driver_smoke(capsys) -> None:
    main()
    output = capsys.readouterr().out
    assert "Phase 13 EXP-120" in output
    assert "documents=22 routes=12 phase11_examples=17 route_families=6" in output
    assert output.count("SHA256 ") == 3
    assert "PASS: IDs, supporting-document references" in output
    assert "not pristine" in output
