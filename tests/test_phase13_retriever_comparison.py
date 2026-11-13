"""EXP-121: independent, hand-checkable retrieval metrics and paired families."""

import pytest

from knowledgebench.evaluation.phase13_retriever_comparison import (
    RetrievalScore,
    aggregate,
    cluster_bootstrap,
    evaluate_rankings,
    paired_family_deltas,
    score_ranking,
)
from knowledgebench.tasks.routing_schema import RoutingBenchmarkTask
from scripts.run_phase10_paired_routing_benchmark import load_tasks
from scripts.run_phase13_fixed_retriever_comparison import (
    K_VALUES,
    assert_frozen_inputs,
    make_rankings,
)


def fake_tasks() -> list[RoutingBenchmarkTask]:
    return [
        RoutingBenchmarkTask(
            task_id="a1",
            pair_id="a",
            query_style="lexical_explicit",
            question="red fox",
            supporting_document_ids={"d1"},
        ),
        RoutingBenchmarkTask(
            task_id="a2",
            pair_id="a",
            query_style="semantic_paraphrase",
            question="fast animal",
            supporting_document_ids={"d1"},
        ),
        RoutingBenchmarkTask(
            task_id="b1",
            pair_id="b",
            query_style="lexical_explicit",
            question="blue whale",
            supporting_document_ids={"d2"},
        ),
        RoutingBenchmarkTask(
            task_id="b2",
            pair_id="b",
            query_style="semantic_paraphrase",
            question="sea mammal",
            supporting_document_ids={"d2"},
        ),
    ]


def sample_rankings() -> dict[str, dict[str, list[str]]]:
    return {
        "bm25": {
            "a1": ["d1", "d2"],
            "a2": ["d1", "d2"],
            "b1": ["d2", "d1"],
            "b2": ["d2", "d1"],
        },
        "hybrid_rrf": {
            "a1": ["d1", "d2"],
            "a2": ["d1", "d2"],
            "b1": ["d1", "d2"],
            "b2": ["d1", "d2"],
        },
    }


def test_hand_computed_recall_rr_and_complete() -> None:
    assert score_ranking(["other", "gold"], {"gold"}, 1) == (0.0, 0.0, False)
    assert score_ranking(["other", "gold"], {"gold"}, 2) == (1.0, 0.5, True)
    assert score_ranking(["a", "b", "c"], {"a", "c"}, 2) == (
        0.5,
        1.0,
        False,
    )
    with pytest.raises(ValueError, match="positive"):
        score_ranking(["gold"], {"gold"}, 0)
    with pytest.raises(ValueError, match="not be empty"):
        score_ranking(["a"], set(), 1)


def test_ranking_aggregates_at_equal_k() -> None:
    scored = evaluate_rankings(fake_tasks(), sample_rankings(), ks=(1, 2))
    assert len(scored) == 16
    metrics = aggregate(scored)
    assert metrics[("bm25", 1)] == (1.0, 1.0, 1.0)
    assert metrics[("hybrid_rrf", 1)] == (0.5, 0.5, 0.5)
    assert metrics[("hybrid_rrf", 2)] == (1.0, 0.75, 1.0)


def test_paired_family_deltas_treat_two_paraphrases_as_one_cluster() -> None:
    scored = evaluate_rankings(fake_tasks(), sample_rankings(), ks=(1, 2))
    deltas = paired_family_deltas(
        scored, better="hybrid_rrf", baseline="bm25", k=2
    )
    assert deltas == {"a": 0.0, "b": -0.5}
    interval = cluster_bootstrap(deltas, draws=1000, seed=121)
    assert interval.mean == -0.25
    assert interval.low <= interval.mean <= interval.high
    assert -0.5 <= interval.low <= interval.high <= 0.0


def test_zero_difference_control_produces_zero_width_ci() -> None:
    values = {f"family-{index}": 0.0 for index in range(6)}
    result = cluster_bootstrap(values, draws=1000, seed=121)
    assert result.mean == result.low == result.high == 0.0


def test_bootstrap_reproducible_and_validates_inputs() -> None:
    diff = {"a": 0.4, "b": -0.2, "c": 0.1}
    assert cluster_bootstrap(diff, draws=500, seed=4) == cluster_bootstrap(
        diff, draws=500, seed=4
    )
    with pytest.raises(ValueError, match="at least one"):
        cluster_bootstrap({})
    with pytest.raises(ValueError, match="positive"):
        cluster_bootstrap({"x": 0.2}, draws=0)


def test_unpaired_family_fails_closed() -> None:
    scores = [
        RetrievalScore("q1", "family", "bm25", 3, 1.0, 1.0, True),
        RetrievalScore("q2", "family", "hybrid", 3, 1.0, 1.0, True),
    ]
    with pytest.raises(ValueError, match="non-paired"):
        paired_family_deltas(scores, better="hybrid", baseline="bm25")


def test_duplicate_or_missing_ranking_fails_closed() -> None:
    tasks = fake_tasks()
    with pytest.raises(ValueError, match="missing or extra"):
        evaluate_rankings(tasks, {"bm25": {"a1": ["d1"]}})
    bad = sample_rankings()
    bad["bm25"]["a1"] = ["d1", "d1"]
    with pytest.raises(ValueError, match="duplicate retrieved"):
        evaluate_rankings(tasks, bad)


def test_pure_ranker_uses_existing_bm25_cosine_and_rrf() -> None:
    tasks = fake_tasks()[:2]
    ids = ["d1", "d2"]
    texts = ["red fox", "blue whale"]
    doc_vectors = [[1.0, 0.0], [0.0, 1.0]]
    query_vectors = [[1.0, 0.0], [0.0, 1.0]]
    rankings = make_rankings(ids, texts, tasks, doc_vectors, query_vectors)
    assert rankings["bm25"]["a1"][0] == "d1"
    assert rankings["dense"]["a1"][0] == "d1"
    assert rankings["dense"]["a2"][0] == "d2"
    assert len(rankings["hybrid_rrf"]["a2"]) == 2
    assert all(len(ranking) == 2 for method in rankings.values() for ranking in method.values())


def test_malformed_embedding_counts_rejected() -> None:
    with pytest.raises(ValueError, match="document/embedding"):
        make_rankings(["d1"], ["one"], fake_tasks()[:1], [], [[1.0]])
    with pytest.raises(ValueError, match="task/embedding"):
        make_rankings(["d1"], ["one"], fake_tasks()[:1], [[1.0]], [])


def test_real_data_checksum_and_six_families() -> None:
    assert_frozen_inputs()
    tasks = load_tasks()
    assert len(tasks) == 12
    assert len({task.pair_id for task in tasks}) == 6
    assert K_VALUES == (1, 2, 3, 5)
