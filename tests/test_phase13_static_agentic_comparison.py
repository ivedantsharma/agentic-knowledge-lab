"""EXP-123: shared search protocol, accounting, and gold isolation tests."""

from dataclasses import replace

import pytest

from knowledgebench.evaluation.phase13_static_agentic_comparison import (
    ARM_NAMES,
    aggregate_grades,
    grade_traces,
    run_arm,
)
from scripts.run_phase13_static_agentic_comparison import load_and_validate_inputs


class FakeBackend:
    def __init__(self, ranking=None):
        self.ranking = ranking or ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        self.calls = []

    def search(self, query, top_k=3):
        self.calls.append((query, top_k))
        return [(item, float(-index)) for index, item in enumerate(self.ranking[:top_k])]


def _inputs():
    documents, tasks, hashes = load_and_validate_inputs()
    return {doc.document_id: doc.text for doc in documents}, tasks, hashes


def test_real_sources_have_expected_gold_and_hashes():
    docs, tasks, hashes = _inputs()
    assert len(docs) == 19
    assert len(tasks) == 5
    assert sorted(task.task_id for task in tasks) == [
        "mh-001", "mh-002", "mh-003", "mh-004", "ood-001"
    ]
    assert len(hashes) == 2
    assert all(len(sha) == 64 for sha in hashes.values())
    assert all(
        all(hop.expected_document_id in docs for hop in task.hops)
        for task in tasks
    )


def test_static_one_call_top3_vs_top9():
    backend = FakeBackend()
    docs = {name: name for name in backend.ranking}
    a = run_arm(
        question="test", task_id="x", arm="static_top3",
        backend=backend, document_texts=docs,
    )
    b = run_arm(
        question="test", task_id="x", arm="static_top9",
        backend=backend, document_texts=docs,
    )
    assert a.calls == b.calls == 1
    assert a.all_retrieved_ids == {"a", "b", "c"}
    assert len(b.all_retrieved_ids) == 9
    assert backend.calls == [("test", 3), ("test", 9)]


def test_static_repeat_three_calls_distinguishable_from_one_call():
    backend = FakeBackend()
    out = run_arm(
        question="Where?", task_id="x", arm="static_repeat3",
        backend=backend, document_texts={x: x for x in backend.ranking},
    )
    assert out.calls == 3
    assert len(out.all_retrieved_ids) == 3
    assert len(out.observed_top1) == 3
    assert out.queries == ("Where?", "Where?", "Where?")


def test_planner_uses_only_observed_text_and_query_not_gold():
    docs = {
        "org_atlas": "Atlas is operated by the Platform Reliability team.",
        "org_platform_reliability": (
            "Platform Reliability maintains the Borealis storage system "
            "for production customer profile data."
        ),
        "manual_borealis": (
            "For the production Borealis service, full backups run every Sunday. "
            "Incremental backups run every six hours."
        ),
    }

    class ChainBackend:
        def search(self, query, top_k=3):
            if "team operates Atlas" in query:
                name = "org_atlas"
            elif "storage system is maintained" in query:
                name = "org_platform_reliability"
            else:
                name = "manual_borealis"
            return [(name, 1.0)]

    question = (
        "What backup cadence is used by the storage system maintained "
        "by the team that operates Atlas?"
    )
    result = run_arm(
        question=question, task_id="x", arm="rule_agent3",
        backend=ChainBackend(), document_texts=docs,
    )
    assert result.calls == 3
    assert result.stopped
    assert not result.planner_failed
    assert result.observed_top1 == (
        "org_atlas", "org_platform_reliability", "manual_borealis"
    )
    assert "Borealis" in result.queries[-1]


def test_agent_same_search_actions_when_gold_labels_change():
    docs, tasks, _ = _inputs()
    backend = FakeBackend(list(docs))
    task = tasks[0]
    first = run_arm(
        question=task.question, task_id=task.task_id, arm="rule_agent3",
        backend=backend, document_texts=docs,
    )
    changed = task.model_copy(update={
        "expected_answer": "invalid gold",
        "hops": [],
    })
    second = run_arm(
        question=changed.question, task_id=changed.task_id, arm="rule_agent3",
        backend=backend, document_texts=docs,
    )
    assert first == second


def test_evaluator_sees_all_returned_hits_not_just_top1():
    _, tasks, _ = _inputs()
    backend = FakeBackend([
        "org_atlas", "org_platform_reliability", "manual_borealis",
        "org_dev_productivity", "manual_cirrus", "org_helios",
        "org_identity_foundations", "manual_solstice", "manual_meridian",
    ])
    docs = {name: name for name in backend.ranking}
    traces = [
        run_arm(
            question=task.question, task_id=task.task_id,
            arm=arm, backend=backend, document_texts=docs,
        )
        for task in tasks for arm in ARM_NAMES
    ]
    scores = grade_traces(tasks, traces)
    target = next(
        score for score in scores
        if score.task_id == "mh-001" and score.arm == "static_top3"
    )
    assert target.complete
    assert target.recall == 1.0
    assert target.unique_docs == 3
    assert not target.stopped
    assert len(scores) == 20
    assert set(aggregate_grades(scores)) == set(ARM_NAMES)


def test_missing_or_duplicated_runs_rejected():
    _, tasks, _ = _inputs()
    docs = {x: x for x in "abcdefghi"}
    traces = [
        run_arm(
            question=task.question, task_id=task.task_id,
            arm=arm, backend=FakeBackend(), document_texts=docs,
        )
        for task in tasks for arm in ARM_NAMES
    ]
    with pytest.raises(ValueError, match="missing, extra, or duplicate"):
        grade_traces(tasks, traces[:-1])
    with pytest.raises(ValueError, match="missing, extra, or duplicate"):
        grade_traces(tasks, [*traces, traces[0]])


def test_invalid_backend_hits_and_bad_trace_are_rejected():
    class InvalidBackend:
        def search(self, query, top_k=3):
            return [("a", 1.0), ("a", 0.5)]

    with pytest.raises(ValueError, match="invalid search output"):
        run_arm(
            question="q", task_id="x", arm="static_top3",
            backend=InvalidBackend(), document_texts={"a": "evidence"},
        )
    _, tasks, _ = _inputs()
    docs = {x: x for x in "abcdefghi"}
    traces = [
        run_arm(
            question=task.question, task_id=task.task_id,
            arm=arm, backend=FakeBackend(), document_texts=docs,
        )
        for task in tasks for arm in ARM_NAMES
    ]
    traces[0] = replace(traces[0], observed_top1=("wrong",))
    with pytest.raises(ValueError, match="observation mismatch"):
        grade_traces(tasks, traces)


def test_unknown_arm_rejected():
    with pytest.raises(ValueError, match="unknown experimental arm"):
        run_arm(
            question="q", task_id="x", arm="not_an_arm",
            backend=FakeBackend(), document_texts={"a": "a"},
        )
