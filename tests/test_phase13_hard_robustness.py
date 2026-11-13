"""EXP-125 robust retrieval: grading integrity and real-source smoke checks."""

import numpy as np
import pytest

from knowledgebench.evaluation.phase13_hard_robustness import (
    evaluate_rankings,
    summarize_cases,
)
from scripts.run_phase13_hard_robustness_comparison import (
    compute_rankings,
    load_inputs,
)


class FakeEncoder:
    def encode(self, value):
        def vector(text):
            raw = text.casefold().encode("utf-8")
            return np.array([
                float(sum(raw[::2]) + 1),
                float(sum(raw[1::2]) + 1),
                float(len(raw) + 1),
            ])
        if isinstance(value, str):
            return vector(value)
        return np.asarray([vector(text) for text in value])


def test_real_hard_sources_and_injection_inventory():
    docs, tasks, injections, hashes = load_inputs()
    assert len(docs) == 22
    assert len(tasks) == 10
    assert len(injections["cases"]) == 4
    assert len(hashes) == 3
    assert all(len(digest) == 64 for digest in hashes.values())


def test_real_bm25_dense_hybrid_adapters_and_grader():
    docs, tasks, _, _ = load_inputs()
    rankings = compute_rankings(docs, tasks, encoder=FakeEncoder())
    assert set(rankings) == {"bm25", "dense", "hybrid_rrf"}
    ids = {doc.document_id for doc in docs}
    assert all(
        len(ranked) == len(docs) and len(set(ranked)) == len(docs)
        for method in rankings.values() for ranked in method.values()
    )
    scored = evaluate_rankings(
        tasks, rankings, document_ids=ids, k_values=(1, 3, 5)
    )
    assert len(scored) == 3 * 10 * 3
    summaries = summarize_cases(scored)
    assert len(summaries) == 9
    assert all(row.answerable_count == 6 for row in summaries)
    assert all(row.unanswerable_count == 4 for row in summaries)
    assert all(0 <= row.mean_support_recall <= 1 for row in summaries)


def test_k_increases_cannot_reduce_gold_recall_or_risk_exposure():
    docs, tasks, _, _ = load_inputs()
    rankings = compute_rankings(docs, tasks, encoder=FakeEncoder())
    rows = evaluate_rankings(
        tasks, rankings, document_ids={doc.document_id for doc in docs},
        k_values=(1, 3, 5),
    )
    for method in rankings:
        for task in tasks:
            samples = sorted(
                (row for row in rows if row.method == method and row.task_id == task.task_id),
                key=lambda row: row.k,
            )
            recalls = [row.support_recall for row in samples]
            if task.should_answer:
                assert recalls == sorted(recalls)
            for label in ("distractor", "contradiction", "stale"):
                present = [dict(row.risk_hits)[label] for row in samples]
                if present[0] is not None:
                    assert present == sorted(present)


def test_unanswerable_retrieval_not_treated_as_answer_or_abstention():
    docs, tasks, _, _ = load_inputs()
    rankings = compute_rankings(docs, tasks, encoder=FakeEncoder())
    rows = evaluate_rankings(
        tasks, rankings, document_ids={doc.document_id for doc in docs},
    )
    unanswerable = [row for row in rows if not row.should_answer]
    assert unanswerable
    assert all(row.support_recall is None for row in unanswerable)
    assert all(row.complete_support is None for row in unanswerable)
    assert all(row.reciprocal_rank is None for row in unanswerable)


def test_missing_labeled_source_fails_closed():
    docs, tasks, _, _ = load_inputs()
    rankings = compute_rankings(docs, tasks, encoder=FakeEncoder())
    with pytest.raises(ValueError, match="unknown source document"):
        evaluate_rankings(
            [replace_model(tasks[0], distractor_document_ids={"missing"}), *tasks[1:]],
            rankings, document_ids={doc.document_id for doc in docs},
        )


def replace_model(task, **changes):
    return task.model_copy(update=changes)


def test_duplicate_or_unknown_rankings_rejected():
    docs, tasks, _, _ = load_inputs()
    rankings = compute_rankings(docs, tasks, encoder=FakeEncoder())
    document_ids = {doc.document_id for doc in docs}
    modified = {
        method: {key: list(value) for key, value in runs.items()}
        for method, runs in rankings.items()
    }
    modified["bm25"][tasks[0].task_id][0] = "unknown"
    with pytest.raises(ValueError, match="ranking contains"):
        evaluate_rankings(tasks, modified, document_ids=document_ids)
    modified["bm25"][tasks[0].task_id][0] = modified["bm25"][tasks[0].task_id][1]
    with pytest.raises(ValueError, match="ranking contains"):
        evaluate_rankings(tasks, modified, document_ids=document_ids)


def test_invalid_k_fails_closed():
    docs, tasks, _, _ = load_inputs()
    rankings = compute_rankings(docs, tasks, encoder=FakeEncoder())
    with pytest.raises(ValueError, match="invalid K"):
        evaluate_rankings(
            tasks, rankings, document_ids={doc.document_id for doc in docs},
            k_values=(1, 0),
        )


def test_conditional_risk_denominators_not_total_tasks():
    docs, tasks, _, _ = load_inputs()
    rankings = compute_rankings(docs, tasks, encoder=FakeEncoder())
    rows = evaluate_rankings(
        tasks, rankings, document_ids={doc.document_id for doc in docs},
    )
    for summary in summarize_cases(rows):
        count_by_type = dict(summary.risk_label_counts)
        assert count_by_type["stale"] == sum(
            bool(task.stale_document_ids) for task in tasks
        )
        assert count_by_type["contradiction"] == sum(
            bool(task.contradicting_document_ids) for task in tasks
        )
        assert count_by_type["distractor"] == sum(
            bool(task.distractor_document_ids) for task in tasks
        )
