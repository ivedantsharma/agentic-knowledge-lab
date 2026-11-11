from knowledgebench.evaluation.routing_evaluator import (
    RetrievalStrategyTaskScore,
    evaluate_routing_oracle,
)


def test_oracle_selects_best_strategy_per_task() -> None:
    scores = [
        RetrievalStrategyTaskScore(
            strategy="bm25",
            task_id="t1",
            supporting_recall=1.0,
            reciprocal_rank=1.0,
            evidence_chain_coverage=1.0,
        ),
        RetrievalStrategyTaskScore(
            strategy="dense",
            task_id="t1",
            supporting_recall=0.5,
            reciprocal_rank=1.0,
            evidence_chain_coverage=0.5,
        ),
        RetrievalStrategyTaskScore(
            strategy="bm25",
            task_id="t2",
            supporting_recall=0.5,
            reciprocal_rank=0.5,
            evidence_chain_coverage=0.5,
        ),
        RetrievalStrategyTaskScore(
            strategy="dense",
            task_id="t2",
            supporting_recall=1.0,
            reciprocal_rank=1.0,
            evidence_chain_coverage=1.0,
        ),
    ]

    report = evaluate_routing_oracle(scores)

    assert report.mean_oracle_supporting_recall == 1.0
    assert report.unique_winner_counts == {
        "bm25": 1,
        "dense": 1,
    }


def test_oracle_records_ties() -> None:
    scores = [
        RetrievalStrategyTaskScore(
            strategy="bm25",
            task_id="t1",
            supporting_recall=1.0,
            reciprocal_rank=1.0,
            evidence_chain_coverage=1.0,
        ),
        RetrievalStrategyTaskScore(
            strategy="dense",
            task_id="t1",
            supporting_recall=1.0,
            reciprocal_rank=1.0,
            evidence_chain_coverage=1.0,
        ),
    ]

    report = evaluate_routing_oracle(scores)

    assert report.tied_tasks == 1
    assert report.comparisons[0].best_strategies == (
        "bm25",
        "dense",
    )
