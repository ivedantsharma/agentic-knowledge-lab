"""EXP-118: BM25 family-split evaluation must not leak test evidence."""

from pathlib import Path

import pytest

from knowledge_engine.rl.reinforce import TabularSoftmaxPolicy, train_reinforce
from knowledge_engine.rl.retrieval_environment import RetrievalRLAction as A
from scripts.run_phase12_family_disjoint_transfer import (
    TRAIN_FAMILY,
    RankedTask,
    family_split,
    fixed_score,
    load_ranked_tasks,
    main,
    model_score,
    task_kwargs,
)


@pytest.fixture(scope="module")
def actual_tasks() -> tuple[RankedTask, ...]:
    return load_ranked_tasks()


def test_loads_twelve_real_tasks_in_six_families(actual_tasks) -> None:
    assert len(actual_tasks) == 12
    assert len({task.family for task in actual_tasks}) == 6
    assert all(task.supporting_ids.issubset(set(task.ranked_ids)) for task in actual_tasks)


def test_family_split_is_disjoint(actual_tasks) -> None:
    train, heldout = family_split(actual_tasks)
    assert {task.task_id for task in train} == {"route-003", "route-004"}
    assert len(heldout) == 10
    assert {task.family for task in train} == {TRAIN_FAMILY}
    assert not {t.family for t in train} & {t.family for t in heldout}


def test_bm25_rank_is_recomputed_not_frozen_hybrid(actual_tasks) -> None:
    ranks = {t.task_id: t.support_rank for t in actual_tasks}
    assert ranks["route-003"] == 1  # frozen EXP-117 HYBRID had support at rank 2
    assert ranks["route-006"] == 3
    assert ranks["route-007"] == 2
    assert ranks["route-008"] == 2
    assert ranks["route-011"] == 1


def test_heldout_contains_different_budget_demands(actual_tasks) -> None:
    _train, heldout = family_split(actual_tasks)
    assert {task.support_rank for task in heldout} == {1, 2, 3}
    assert all(task.support_rank <= 5 for task in heldout)


def test_fixed_k1_cannot_complete_solstice_paraphrase(actual_tasks) -> None:
    task = next(t for t in actual_tasks if t.task_id == "route-006")
    _score1, coverage1 = fixed_score(task, (A.SEARCH_K1, A.STOP))
    _score3, coverage3 = fixed_score(task, (A.SEARCH_K3, A.STOP))
    assert coverage1 == 0.0
    assert coverage3 == 1.0


def test_policy_has_no_gold_features_during_actions(actual_tasks) -> None:
    task = next(t for t in actual_tasks if t.task_id == "route-001")
    assert set(task_kwargs(task)) == {"question", "ranked_ids", "supporting_ids"}
    # Environment receives support IDs for reward; policy keys use only
    # the public observation's requested_k and steps_taken.
    model = TabularSoftmaxPolicy()
    result = model_score(model, task, episodes=20, seed=5)
    assert len(result) == 3
    assert all(isinstance(item, float) for item in result)


def test_training_same_cirrus_trajectory_does_not_use_heldout(actual_tasks) -> None:
    train, heldout = family_split(actual_tasks)
    training = next(t for t in train if t.task_id == "route-003")
    model = TabularSoftmaxPolicy()
    first = model_score(model, heldout[0], episodes=50, seed=119)
    history = train_reinforce(
        policy=model, **task_kwargs(training), episodes=100, seed=118
    )
    second = model_score(model, heldout[0], episodes=50, seed=119)
    assert history.episodes == 100
    assert all(t.family != training.family for t in heldout)
    assert first != second  # policy updates affect the heldout distribution


def test_invalid_split_detected(actual_tasks) -> None:
    with pytest.raises(ValueError, match="nonempty"):
        family_split(actual_tasks, train_family="unseen_family")
    with pytest.raises(ValueError, match="nonempty"):
        family_split(tuple(t for t in actual_tasks if t.family == TRAIN_FAMILY))


def test_invalid_support_ids_are_rejected(tmp_path: Path) -> None:
    documents = tmp_path / "docs.json"
    tasks = tmp_path / "tasks.json"
    documents.write_text('[{"document_id":"doc-a","text":"test"}]')
    tasks.write_text(
        '[{"task_id":"test-1","pair_id":"family-a",'
        '"question":"test","supporting_document_ids":["unknown"]}]'
    )
    with pytest.raises(ValueError, match="supporting documents"):
        load_ranked_tasks(documents, tasks)


def test_exp118_driver_smoke_with_real_data(monkeypatch, capsys) -> None:
    from scripts import run_phase12_family_disjoint_transfer as driver

    monkeypatch.setattr(driver, "SEEDS", (0,))
    monkeypatch.setattr(driver, "TRAIN_EPISODES", 30)
    monkeypatch.setattr(driver, "EVAL_EPISODES", 30)
    main()
    output = capsys.readouterr().out
    assert "Phase 12 EXP-118" in output
    assert "heldout_mean_G_after=" in output
    assert "heldout_gap_to_oracle=" in output
    assert "route-006 family=solstice_cache max_support_rank=3" in output
