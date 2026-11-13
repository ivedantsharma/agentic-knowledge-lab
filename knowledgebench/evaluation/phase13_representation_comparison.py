"""EXP-122 B2: score *retrieved* evidence atoms with evaluator-only gold.

Candidate systems do not receive expected paths, answers or evidence atom IDs.
This module maps returned source references back to auditable evidence atoms.
"""

from dataclasses import dataclass
from statistics import fmean

from knowledgebench.datasets.representation_bridge import CommonRepresentationSubstrate


@dataclass(frozen=True)
class SystemEvidenceResult:
    task_id: str
    system: str
    atom_ids: tuple[str, ...]
    words_returned: int
    candidates_scored: int
    answer: str | None = None
    claim_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class SystemEvidenceScore:
    task_id: str
    system: str
    coverage: float
    complete: bool
    evidence_count: int
    words_returned: int
    candidates_scored: int
    answer_correct: bool | None
    claim_path_correct: bool | None


def evaluate_system_outputs(
    substrate: CommonRepresentationSubstrate,
    outputs: list[SystemEvidenceResult],
    *,
    budget: int = 3,
) -> list[SystemEvidenceScore]:
    if budget <= 0:
        raise ValueError("budget must be positive")
    tasks = {task.task_id: task for task in substrate.tasks}
    atoms = {atom.atom_id: atom for atom in substrate.atoms}
    expected_keys = {(task.task_id, system) for task in substrate.tasks
                     for system in ("flat_bm25", "hierarchy", "graph")}
    observed = {(out.task_id, out.system) for out in outputs}
    if len(outputs) != len(observed) or observed != expected_keys:
        raise ValueError("missing, extra or duplicated system-task outcomes")
    scores = []
    for out in outputs:
        if (len(out.atom_ids) > budget or len(set(out.atom_ids)) != len(out.atom_ids)
                or not set(out.atom_ids).issubset(atoms)):
            raise ValueError("unrecognized, repeated or over-budget evidence")
        if out.words_returned < 0 or out.candidates_scored < 0:
            raise ValueError("invalid resource accounting")
        if out.system != "graph" and (out.answer is not None or out.claim_ids):
            raise ValueError("flat/hierarchy must not contain generated answers")
        expected = set(tasks[out.task_id].expected_claim_ids)
        found = {atoms[atom_id].claim_id for atom_id in out.atom_ids}
        correct = found & expected
        task = tasks[out.task_id]
        scores.append(
            SystemEvidenceScore(
                task_id=out.task_id,
                system=out.system,
                coverage=len(correct) / len(expected),
                complete=expected.issubset(found),
                evidence_count=len(out.atom_ids),
                words_returned=out.words_returned,
                candidates_scored=out.candidates_scored,
                answer_correct=(
                    out.answer.casefold() == task.expected_answer.casefold()
                    if out.system == "graph" and out.answer is not None
                    else False if out.system == "graph" else None
                ),
                claim_path_correct=(
                    out.claim_ids == tuple(task.expected_claim_ids)
                    if out.system == "graph" else None
                ),
            )
        )
    return scores


def summarize_scores(scores: list[SystemEvidenceScore]) -> dict[str, dict[str, float]]:
    return {
        system: {
            "mean_claim_coverage": fmean(x.coverage for x in scores if x.system == system),
            "complete_fraction": fmean(float(x.complete) for x in scores if x.system == system),
            "mean_evidence_count": fmean(x.evidence_count for x in scores if x.system == system),
            "mean_output_words": fmean(x.words_returned for x in scores if x.system == system),
            "mean_candidates_scored": fmean(x.candidates_scored for x in scores if x.system == system),
        }
        for system in ("flat_bm25", "hierarchy", "graph")
    }
