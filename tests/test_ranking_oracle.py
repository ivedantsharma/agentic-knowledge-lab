from knowledgebench.evaluation.ranking_oracle import (
    RankingStrategyScore,
    evaluate_ranking_oracle,
)


def test_ranking_oracle_uses_best_rr_per_task() -> None:
    report = evaluate_ranking_oracle(
        [
            RankingStrategyScore(
                task_id="t1",
                strategy="bm25",
                reciprocal_rank=1.0,
            ),
            RankingStrategyScore(
                task_id="t1",
                strategy="dense",
                reciprocal_rank=0.5,
            ),
            RankingStrategyScore(
                task_id="t2",
                strategy="bm25",
                reciprocal_rank=0.5,
            ),
            RankingStrategyScore(
                task_id="t2",
                strategy="dense",
                reciprocal_rank=1.0,
            ),
        ]
    )

    assert report.oracle_mrr == 1.0
    assert report.unique_winner_counts == {
        "bm25": 1,
        "dense": 1,
    }


def test_ranking_oracle_records_ties() -> None:
    report = evaluate_ranking_oracle(
        [
            RankingStrategyScore(
                task_id="t1",
                strategy="bm25",
                reciprocal_rank=1.0,
            ),
            RankingStrategyScore(
                task_id="t1",
                strategy="dense",
                reciprocal_rank=1.0,
            ),
        ]
    )

    assert report.tied_tasks == 1
    assert report.task_reports[0].best_strategies == (
        "bm25",
        "dense",
    )
