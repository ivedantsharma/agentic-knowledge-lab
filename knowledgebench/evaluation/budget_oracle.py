from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetTaskResult:
    task_id: str
    minimal_k_for_max_recall: int
    max_recall: float
    recall_by_k: dict[int, float]


@dataclass(frozen=True)
class BudgetOracleReport:
    tasks: int
    mean_minimal_k: float
    max_required_k: int
    task_results: tuple[BudgetTaskResult, ...]


def minimal_k_for_max_recall(
    task_id: str,
    ranked_ids: list[str],
    supporting_ids: set[str],
    candidate_ks: tuple[int, ...],
) -> BudgetTaskResult:
    if not supporting_ids:
        raise ValueError(
            "supporting_ids must not be empty"
        )

    recall_by_k = {
        k: (
            len(
                set(ranked_ids[:k])
                & supporting_ids
            )
            / len(supporting_ids)
        )
        for k in candidate_ks
    }

    max_recall = max(
        recall_by_k.values()
    )

    minimal_k = min(
        k
        for k, recall
        in recall_by_k.items()
        if recall == max_recall
    )

    return BudgetTaskResult(
        task_id=task_id,
        minimal_k_for_max_recall=minimal_k,
        max_recall=max_recall,
        recall_by_k=recall_by_k,
    )


def evaluate_budget_oracle(
    results: list[BudgetTaskResult],
) -> BudgetOracleReport:
    return BudgetOracleReport(
        tasks=len(results),
        mean_minimal_k=(
            sum(
                result.minimal_k_for_max_recall
                for result in results
            )
            / len(results)
            if results
            else 0.0
        ),
        max_required_k=(
            max(
                result.minimal_k_for_max_recall
                for result in results
            )
            if results
            else 0
        ),
        task_results=tuple(results),
    )
