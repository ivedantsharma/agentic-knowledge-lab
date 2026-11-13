"""EXP-119: guard against false Phase 11 / Phase 12 comparisons."""

import json

import pytest

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.training.retrieval_policy import RetrievalPolicyAction
from scripts.run_phase12_policy_protocol_audit import (
    SFT_TO_RL,
    audit_shared_tasks,
    first_sufficient_budget,
    main,
    map_first_search_action,
)


def test_budget_mapping_only_has_four_search_actions() -> None:
    assert len(SFT_TO_RL) == 4
    assert map_first_search_action(RetrievalPolicyAction.REFORMULATE) is None
    assert RetrievalRLAction.STOP not in SFT_TO_RL.values()
    assert map_first_search_action(
        RetrievalPolicyAction.SEARCH_HYBRID_K2
    ) == RetrievalRLAction.SEARCH_K2


@pytest.mark.parametrize(
    ("rank", "budget"),
    [(1, 1), (2, 2), (3, 3), (4, 5), (5, 5), (6, None)],
)
def test_minimum_budget_for_gold_rank(rank: int, budget: int | None) -> None:
    assert first_sufficient_budget(rank) == budget


def test_shared_tasks_have_exact_questions_and_real_support_rank() -> None:
    rows = audit_shared_tasks()
    assert len(rows) == 12
    assert {row.task_id for row in rows} == {
        f"route-{i:03d}" for i in range(1, 13)
    }
    assert all(row.bm25_min_budget in (1, 2, 3) for row in rows)


def test_sft_splits_differ_from_rl_family_holdout() -> None:
    rows = {row.task_id: row for row in audit_shared_tasks()}
    assert rows["route-001"].sft_split == "dev"
    assert rows["route-005"].sft_split == "train"
    assert rows["route-007"].sft_split == "heldout"
    assert rows["route-009"].sft_split == "train"
    assert rows["route-011"].sft_split == "train"
    # RL heldout excludes only Cirrus, unlike the Phase 11 family split.
    assert rows["route-003"].evidence_family_rl == "cirrus_retry"


def test_retriever_mismatch_is_observable_on_cirrus() -> None:
    rows = {row.task_id: row for row in audit_shared_tasks()}
    assert rows["route-003"].sft_target_budget == 2
    assert rows["route-003"].bm25_min_budget == 1
    assert rows["route-003"].budget_matches_bm25 is False


def test_retriever_mismatch_is_observable_on_solstice_paraphrase() -> None:
    rows = {row.task_id: row for row in audit_shared_tasks()}
    assert rows["route-006"].sft_target_budget == 2
    assert rows["route-006"].bm25_min_budget == 3
    assert rows["route-006"].budget_matches_bm25 is False


def test_duplicate_sft_source_ids_fail_closed(tmp_path) -> None:
    existing = audit_shared_tasks()
    assert existing
    dataset = [
        {
            "source_task_id": "route-003",
            "question": "What is the production Cirrus retry limit before dead-letter handling?",
            "target_action": "SEARCH_HYBRID_K2",
            "evidence_family": "cirrus",
            "split": "train",
        }
    ]
    path = tmp_path / "dupe.json"
    path.write_text(json.dumps([*dataset, *dataset]))
    with pytest.raises(ValueError, match="duplicate SFT source"):
        audit_shared_tasks(sft_path=path)


def test_question_mismatch_fails_closed(tmp_path) -> None:
    path = tmp_path / "different-question.json"
    path.write_text(
        json.dumps(
            [
                {
                    "source_task_id": "route-003",
                    "question": "an altered question",
                    "target_action": "SEARCH_HYBRID_K2",
                    "evidence_family": "cirrus",
                    "split": "train",
                }
            ]
        )
    )
    with pytest.raises(ValueError, match="question differs"):
        audit_shared_tasks(sft_path=path)


def test_exp119_driver_smoke(capsys) -> None:
    main()
    output = capsys.readouterr().out
    assert "Phase 12 EXP-119" in output
    assert "shared_tasks=12" in output
    assert "direct Phase-11 LoRA-vs-Phase-12 RL performance claims are invalid" in output
    assert "budget_mismatches=" in output
