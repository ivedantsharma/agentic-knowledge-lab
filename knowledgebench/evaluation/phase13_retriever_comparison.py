"""Pure Phase 13 fixed-retriever metrics and family-cluster uncertainty.

Retriever rankings must be constructed without gold. This module only scores
finished rankings against evaluator labels and resamples evidence families.
"""

from collections import defaultdict
from dataclasses import dataclass
from random import Random
from statistics import fmean

from knowledgebench.tasks.routing_schema import RoutingBenchmarkTask


@dataclass(frozen=True)
class RetrievalScore:
    task_id: str
    family: str
    method: str
    k: int
    recall: float
    reciprocal_rank: float
    complete: bool


@dataclass(frozen=True)
class Interval:
    mean: float
    low: float
    high: float


def score_ranking(
    ranked_ids: list[str] | tuple[str, ...],
    supporting_ids: set[str],
    k: int,
) -> tuple[float, float, bool]:
    if k <= 0:
        raise ValueError("k must be positive")
    if not supporting_ids:
        raise ValueError("support must not be empty for answerable retrieval")
    top = ranked_ids[:k]
    recall = len(set(top) & supporting_ids) / len(supporting_ids)
    rank = next(
        (i for i, doc_id in enumerate(top, start=1) if doc_id in supporting_ids),
        None,
    )
    return recall, (1.0 / rank if rank is not None else 0.0), recall == 1.0


def evaluate_rankings(
    tasks: list[RoutingBenchmarkTask],
    rankings: dict[str, dict[str, list[str]]],
    ks: tuple[int, ...] = (1, 2, 3, 5),
) -> list[RetrievalScore]:
    """Fail closed on missing tasks, duplicate IDs or invalid ranking entries."""
    task_ids = [task.task_id for task in tasks]
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("duplicate task IDs")
    if not rankings:
        raise ValueError("at least one retriever is required")
    for method, by_task in rankings.items():
        if set(by_task) != set(task_ids):
            raise ValueError(f"missing or extra tasks in {method}")
        for ranked in by_task.values():
            if len(ranked) != len(set(ranked)):
                raise ValueError("duplicate retrieved document IDs")
    if not ks or any(k <= 0 for k in ks):
        raise ValueError("K must be positive")

    result: list[RetrievalScore] = []
    for task in tasks:
        for method, by_task in rankings.items():
            for k in ks:
                recall, rr, complete = score_ranking(
                    by_task[task.task_id], task.supporting_document_ids, k
                )
                result.append(
                    RetrievalScore(
                        task_id=task.task_id,
                        family=task.pair_id,
                        method=method,
                        k=k,
                        recall=recall,
                        reciprocal_rank=rr,
                        complete=complete,
                    )
                )
    return result


def aggregate(
    scores: list[RetrievalScore],
) -> dict[tuple[str, int], tuple[float, float, float]]:
    grouped: dict[tuple[str, int], list[RetrievalScore]] = defaultdict(list)
    for score in scores:
        grouped[(score.method, score.k)].append(score)
    return {
        key: (
            fmean(item.recall for item in rows),
            fmean(item.reciprocal_rank for item in rows),
            fmean(float(item.complete) for item in rows),
        )
        for key, rows in grouped.items()
    }


def paired_family_deltas(
    scores: list[RetrievalScore],
    *,
    better: str,
    baseline: str,
    k: int = 3,
) -> dict[str, float]:
    """One difference per source family, not two independent paraphrase rows."""
    by_method_family: dict[tuple[str, str], dict[str, float]] = defaultdict(dict)
    for item in scores:
        if item.k != k or item.method not in {better, baseline}:
            continue
        key = (item.method, item.family)
        if item.task_id in by_method_family[key]:
            raise ValueError("repeated task score")
        by_method_family[key][item.task_id] = item.reciprocal_rank
    families = sorted(
        {family for (method, family) in by_method_family if method == better}
        | {family for (method, family) in by_method_family if method == baseline}
    )
    if not families:
        raise ValueError("no paired evidence families")
    deltas = {}
    for family in families:
        better_tasks = by_method_family.get((better, family), {})
        baseline_tasks = by_method_family.get((baseline, family), {})
        if not better_tasks or set(better_tasks) != set(baseline_tasks):
            raise ValueError(f"non-paired tasks for {family}")
        deltas[family] = fmean(
            better_tasks[task_id] - baseline_tasks[task_id]
            for task_id in sorted(better_tasks)
        )
    return deltas


def cluster_bootstrap(
    family_deltas: dict[str, float],
    *,
    draws: int = 10_000,
    seed: int = 121,
) -> Interval:
    """Percentile CI for equal-sized source families (six pairs here)."""
    if not family_deltas:
        raise ValueError("at least one evidence family required")
    if draws <= 0:
        raise ValueError("draws must be positive")
    observations = [family_deltas[key] for key in sorted(family_deltas)]
    rng = Random(seed)
    n = len(observations)
    replicates = sorted(
        fmean(observations[rng.randrange(n)] for _ in range(n))
        for _ in range(draws)
    )
    lo = replicates[int(0.025 * (draws - 1))]
    hi = replicates[int(0.975 * (draws - 1))]
    return Interval(fmean(observations), lo, hi)
