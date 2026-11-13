"""EXP-122 Gate B2: exact evidence-only grading and real adapter smoke tests.

Model fakes are deterministic and do not see evaluator gold. Full pretrained
model scoring remains a separate explicit experiment-driver run.
"""

import hashlib
from dataclasses import replace

import numpy as np
import pytest

from knowledgebench.datasets.representation_bridge import build_common_substrate
from knowledgebench.evaluation.phase13_representation_comparison import (
    SystemEvidenceResult,
    evaluate_system_outputs,
    summarize_scores,
)
from scripts.run_phase13_paired_representation_comparison import (
    MAX_ATOMS,
    run_paired_systems,
)


class FakeEmbedder:
    def encode(self, value):
        def vector(s: str):
            digest = hashlib.sha256(s.encode("utf-8")).digest()
            return np.asarray([float(v + 1) for v in digest[:8]])

        if isinstance(value, str):
            return vector(value)
        return np.asarray([vector(item) for item in value])


class FakeCrossEncoder:
    def predict(self, pairs):
        return np.asarray([
            len(set(query.lower().split()) & set(text.lower().split()))
            for query, text in pairs
        ], dtype=float)


def _perfect_outputs():
    substrate = build_common_substrate()
    by_claim = {atom.claim_id: atom.atom_id for atom in substrate.atoms}
    outcomes = []
    for task in substrate.tasks:
        atoms = tuple(by_claim[claim] for claim in task.expected_claim_ids)
        for system in ("flat_bm25", "hierarchy", "graph"):
            outcomes.append(
                SystemEvidenceResult(
                    task_id=task.task_id,
                    system=system,
                    atom_ids=atoms,
                    words_returned=15,
                    candidates_scored=15,
                    answer=task.expected_answer if system == "graph" else None,
                    claim_ids=tuple(task.expected_claim_ids) if system == "graph" else (),
                )
            )
    return substrate, outcomes


def test_hand_checkable_complete_coverage() -> None:
    substrate, outcomes = _perfect_outputs()
    scores = evaluate_system_outputs(substrate, outcomes, budget=3)
    assert len(scores) == 12
    assert all(x.complete and x.coverage == 1.0 for x in scores)
    report = summarize_scores(scores)
    assert report["flat_bm25"]["mean_claim_coverage"] == 1.0
    assert report["graph"]["complete_fraction"] == 1.0
    assert all(x.answer_correct is True for x in scores if x.system == "graph")
    assert all(x.answer_correct is None for x in scores if x.system != "graph")


def test_partial_evidence_has_fractional_coverage_not_answer_correctness() -> None:
    substrate, outcomes = _perfect_outputs()
    first = outcomes[0]
    outcomes[0] = replace(first, atom_ids=first.atom_ids[:1])
    scores = evaluate_system_outputs(substrate, outcomes, budget=3)
    assert scores[0].coverage == pytest.approx(1 / 3)
    assert not scores[0].complete
    assert scores[0].answer_correct is None


def test_missing_excess_duplicate_or_unknown_evidence_rejected() -> None:
    substrate, outcomes = _perfect_outputs()
    with pytest.raises(ValueError, match="missing, extra"):
        evaluate_system_outputs(substrate, outcomes[:-1])
    with pytest.raises(ValueError, match="missing, extra"):
        evaluate_system_outputs(substrate, [*outcomes, outcomes[0]])
    first = outcomes[0]
    for atoms in (
        ("missing",),
        (first.atom_ids[0], first.atom_ids[0]),
        (*first.atom_ids, "extra"),
    ):
        changed = [replace(first, atom_ids=atoms), *outcomes[1:]]
        with pytest.raises(ValueError, match="unrecognized, repeated or over-budget"):
            evaluate_system_outputs(substrate, changed, budget=3)


def test_flat_and_hierarchy_must_not_claim_answer_generation() -> None:
    substrate, outcomes = _perfect_outputs()
    outcomes[0] = replace(outcomes[0], answer="injected")
    with pytest.raises(ValueError, match="must not contain generated"):
        evaluate_system_outputs(substrate, outcomes)


def test_fake_models_run_three_existing_system_implementations() -> None:
    substrate = build_common_substrate()
    outputs = run_paired_systems(
        substrate,
        embedding_model=FakeEmbedder(),
        cross_encoder=FakeCrossEncoder(),
    )
    assert len(outputs) == 12
    assert {item.system for item in outputs} == {
        "flat_bm25", "hierarchy", "graph"
    }
    assert all(len(item.atom_ids) <= MAX_ATOMS for item in outputs)
    scores = evaluate_system_outputs(substrate, outputs, budget=MAX_ATOMS)
    assert len(scores) == 12
    assert all(0.0 <= item.coverage <= 1.0 for item in scores)
    assert all(item.answer is None for item in outputs if item.system != "graph")
    assert all(item.answer is not None for item in outputs if item.system == "graph")


def test_retrieval_independent_of_evaluator_expected_answer() -> None:
    substrate = build_common_substrate()
    model, reranker = FakeEmbedder(), FakeCrossEncoder()
    original = run_paired_systems(
        substrate, embedding_model=model, cross_encoder=reranker
    )
    modified = replace(
        substrate,
        tasks=tuple(
            task.model_copy(update={
                "expected_answer": "changed gold label",
                "expected_claim_ids": ["changed-claim"],
            })
            for task in substrate.tasks
        ),
    )
    candidate_only = run_paired_systems(
        modified, embedding_model=model, cross_encoder=reranker
    )
    assert original == candidate_only


def test_budget_enforced_before_metrics() -> None:
    substrate, outcomes = _perfect_outputs()
    with pytest.raises(ValueError, match="unrecognized, repeated or over-budget"):
        evaluate_system_outputs(substrate, outcomes, budget=1)
    with pytest.raises(ValueError, match="budget must be positive"):
        evaluate_system_outputs(substrate, outcomes, budget=0)
