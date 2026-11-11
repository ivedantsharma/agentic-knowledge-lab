from dataclasses import dataclass


@dataclass(frozen=True)
class RankingStrategyScore:
    task_id: str
    strategy: str
    reciprocal_rank: float


@dataclass(frozen=True)
class RankingOracleTask:
    task_id: str
    best_reciprocal_rank: float
    best_strategies: tuple[str, ...]


@dataclass(frozen=True)
class RankingOracleReport:
    tasks: int
    oracle_mrr: float
    unique_winner_counts: dict[str, int]
    tied_tasks: int
    task_reports: tuple[RankingOracleTask, ...]


def evaluate_ranking_oracle(
    scores: list[RankingStrategyScore],
) -> RankingOracleReport:
    by_task: dict[
        str,
        list[RankingStrategyScore],
    ] = {}

    for score in scores:
        by_task.setdefault(
            score.task_id,
            [],
        ).append(score)

    reports: list[RankingOracleTask] = []
    unique_winner_counts: dict[str, int] = {}
    tied_tasks = 0

    for task_id in sorted(by_task):
        task_scores = by_task[task_id]
        best_rr = max(
            score.reciprocal_rank
            for score in task_scores
        )

        winners = tuple(
            sorted(
                score.strategy
                for score in task_scores
                if score.reciprocal_rank == best_rr
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

        reports.append(
            RankingOracleTask(
                task_id=task_id,
                best_reciprocal_rank=best_rr,
                best_strategies=winners,
            )
        )

    return RankingOracleReport(
        tasks=len(reports),
        oracle_mrr=(
            sum(
                report.best_reciprocal_rank
                for report in reports
            )
            / len(reports)
            if reports
            else 0.0
        ),
        unique_winner_counts=unique_winner_counts,
        tied_tasks=tied_tasks,
        task_reports=tuple(reports),
    )
