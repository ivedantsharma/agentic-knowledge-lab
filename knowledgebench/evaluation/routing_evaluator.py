from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalStrategyTaskScore:
    strategy: str
    task_id: str
    supporting_recall: float
    reciprocal_rank: float
    evidence_chain_coverage: float


@dataclass(frozen=True)
class RoutingTaskComparison:
    task_id: str
    best_strategies: tuple[str, ...]
    best_supporting_recall: float
    best_reciprocal_rank: float


@dataclass(frozen=True)
class RoutingOracleSummary:
    tasks: int
    mean_oracle_supporting_recall: float
    mean_oracle_reciprocal_rank: float
    unique_winner_counts: dict[str, int]
    tied_tasks: int
    comparisons: tuple[RoutingTaskComparison, ...]


def evaluate_routing_oracle(
    scores: list[RetrievalStrategyTaskScore],
) -> RoutingOracleSummary:
    by_task: dict[
        str,
        list[RetrievalStrategyTaskScore],
    ] = {}

    for score in scores:
        by_task.setdefault(
            score.task_id,
            [],
        ).append(score)

    comparisons: list[RoutingTaskComparison] = []
    unique_winner_counts: dict[str, int] = {}
    tied_tasks = 0

    for task_id in sorted(by_task):
        task_scores = by_task[task_id]

        best_key = max(
            (
                score.supporting_recall,
                score.reciprocal_rank,
            )
            for score in task_scores
        )

        winners = tuple(
            sorted(
                score.strategy
                for score in task_scores
                if (
                    score.supporting_recall,
                    score.reciprocal_rank,
                )
                == best_key
            )
        )

        if len(winners) == 1:
            winner = winners[0]
            unique_winner_counts[winner] = (
                unique_winner_counts.get(
                    winner,
                    0,
                )
                + 1
            )
        else:
            tied_tasks += 1

        comparisons.append(
            RoutingTaskComparison(
                task_id=task_id,
                best_strategies=winners,
                best_supporting_recall=best_key[0],
                best_reciprocal_rank=best_key[1],
            )
        )

    task_count = len(comparisons)

    return RoutingOracleSummary(
        tasks=task_count,
        mean_oracle_supporting_recall=(
            sum(
                item.best_supporting_recall
                for item in comparisons
            )
            / task_count
            if task_count
            else 0.0
        ),
        mean_oracle_reciprocal_rank=(
            sum(
                item.best_reciprocal_rank
                for item in comparisons
            )
            / task_count
            if task_count
            else 0.0
        ),
        unique_winner_counts=unique_winner_counts,
        tied_tasks=tied_tasks,
        comparisons=tuple(comparisons),
    )
