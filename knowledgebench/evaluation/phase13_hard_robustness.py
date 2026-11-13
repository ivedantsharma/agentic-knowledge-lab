"""EXP-125: independent evidence coverage and conditional exposure evaluation.

Unanswerable retrieval and exposure to misleading evidence are diagnostics,
NOT downstream abstention accuracy or demonstrated answer contamination.
"""

from dataclasses import dataclass
from statistics import fmean

from knowledgebench.tasks.v2_schema import KnowledgeBenchV2Task

RISK_LABELS = ("distractor", "contradiction", "stale")


@dataclass(frozen=True)
class RobustnessCase:
    task_id: str
    method: str
    k: int
    retrieved_ids: tuple[str, ...]
    should_answer: bool
    support_recall: float | None
    complete_support: bool | None
    reciprocal_rank: float | None
    risk_hits: tuple[tuple[str, bool | None], ...]
    ambiguity_candidate_coverage: float | None


@dataclass(frozen=True)
class RobustnessSummary:
    method: str
    k: int
    answerable_count: int
    unanswerable_count: int
    mean_support_recall: float
    complete_support_rate: float
    mean_reciprocal_rank: float
    unanswerable_nonempty_retrieval_rate: float
    ambiguity_task_count: int
    mean_ambiguity_coverage: float | None
    risk_label_counts: tuple[tuple[str, int], ...]
    conditional_risk_exposure_rates: tuple[tuple[str, float | None], ...]


def evaluate_rankings(
    tasks: list[KnowledgeBenchV2Task],
    rankings: dict[str, dict[str, list[str]]],
    *,
    document_ids: set[str],
    k_values: tuple[int, ...] = (1, 3, 5),
) -> list[RobustnessCase]:
    if not tasks or not rankings or not document_ids:
        raise ValueError("empty source/benchmark/rankings")
    if len({task.task_id for task in tasks}) != len(tasks):
        raise ValueError("duplicate task ID")
    if not k_values or any(k <= 0 for k in k_values) or len(set(k_values)) != len(k_values):
        raise ValueError("invalid K values")
    task_ids = {task.task_id for task in tasks}
    for task in tasks:
        relevant = set().union(
            task.supporting_document_ids,
            task.distractor_document_ids,
            task.contradicting_document_ids,
            task.stale_document_ids,
            task.ambiguity_candidate_document_ids,
        )
        if not relevant.issubset(document_ids):
            raise ValueError("benchmark references unknown source document")
    for method, results in rankings.items():
        if not method or set(results) != task_ids:
            raise ValueError("missing, extra, or unnamed method/task")
        for ranked in results.values():
            if (
                not ranked or len(set(ranked)) != len(ranked)
                or not set(ranked).issubset(document_ids)
            ):
                raise ValueError("ranking contains empty, duplicate or unknown documents")
            if len(ranked) < max(k_values):
                raise ValueError("rankings too short for requested K")
    rows = []
    for method, results in rankings.items():
        for task in tasks:
            for k in k_values:
                retrieved = tuple(results[task.task_id][:k])
                recovered = set(retrieved)
                support = task.supporting_document_ids
                recall = len(recovered & support) / len(support) if support else None
                rank = next(
                    (1.0 / (i + 1) for i, doc_id in enumerate(retrieved) if doc_id in support),
                    0.0,
                ) if support else None
                risk_sources = {
                    "distractor": task.distractor_document_ids,
                    "contradiction": task.contradicting_document_ids,
                    "stale": task.stale_document_ids,
                }
                rows.append(
                    RobustnessCase(
                        task_id=task.task_id, method=method, k=k,
                        retrieved_ids=retrieved,
                        should_answer=task.should_answer,
                        support_recall=recall,
                        complete_support=support.issubset(recovered) if support else None,
                        reciprocal_rank=rank,
                        risk_hits=tuple(
                            (name, bool(recovered & sources) if sources else None)
                            for name, sources in risk_sources.items()
                        ),
                        ambiguity_candidate_coverage=(
                            len(recovered & task.ambiguity_candidate_document_ids)
                            / len(task.ambiguity_candidate_document_ids)
                            if task.ambiguity_candidate_document_ids else None
                        ),
                    )
                )
    return rows


def summarize_cases(rows: list[RobustnessCase]) -> list[RobustnessSummary]:
    if not rows:
        raise ValueError("empty evaluation rows")
    result = []
    keys = sorted({(row.method, row.k) for row in rows})
    for method, k in keys:
        subset = [row for row in rows if (row.method, row.k) == (method, k)]
        answerable = [row for row in subset if row.should_answer]
        unanswerable = [row for row in subset if not row.should_answer]
        ambiguous = [
            row.ambiguity_candidate_coverage
            for row in subset
            if row.ambiguity_candidate_coverage is not None
        ]
        risk_denominators = []
        risk_rates = []
        for name in RISK_LABELS:
            hits = [dict(row.risk_hits)[name] for row in subset]
            labeled = [hit for hit in hits if hit is not None]
            risk_denominators.append((name, len(labeled)))
            risk_rates.append((
                name, fmean(float(hit) for hit in labeled) if labeled else None,
            ))
        result.append(RobustnessSummary(
            method=method, k=k,
            answerable_count=len(answerable),
            unanswerable_count=len(unanswerable),
            mean_support_recall=fmean(
                row.support_recall for row in answerable if row.support_recall is not None
            ) if answerable else 0.0,
            complete_support_rate=fmean(
                float(row.complete_support) for row in answerable
            ) if answerable else 0.0,
            mean_reciprocal_rank=fmean(
                row.reciprocal_rank for row in answerable if row.reciprocal_rank is not None
            ) if answerable else 0.0,
            unanswerable_nonempty_retrieval_rate=fmean(
                float(bool(row.retrieved_ids)) for row in unanswerable
            ) if unanswerable else 0.0,
            ambiguity_task_count=len(ambiguous),
            mean_ambiguity_coverage=fmean(ambiguous) if ambiguous else None,
            risk_label_counts=tuple(risk_denominators),
            conditional_risk_exposure_rates=tuple(risk_rates),
        ))
    return result
