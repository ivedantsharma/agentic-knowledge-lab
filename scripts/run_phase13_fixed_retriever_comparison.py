"""EXP-121: BM25 vs MiniLM dense vs RRF under one frozen protocol.

No policy training. Phase 10 paired queries are *previously inspected*
development tasks, not pristine external generalization evidence.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.hybrid import reciprocal_rank_fusion
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledgebench.evaluation.phase13_retriever_comparison import (
    aggregate,
    cluster_bootstrap,
    evaluate_rankings,
    paired_family_deltas,
)
from knowledgebench.tasks.routing_schema import RoutingBenchmarkTask
from scripts.run_phase10_paired_routing_benchmark import (
    load_documents,
    load_tasks,
)
from scripts.run_phase13_campaign_inventory import build_inventory

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
K_VALUES = (1, 2, 3, 5)
RRF_K = 60
SHA256 = {
    "knowledgebench_v2_hard_documents_v0.json":
        "9015e8924fffcb461a7278c24e7f108d7a33377fcb6967d0f7bf0539fe9022be",
    "phase10_routing_pairs_v0.json":
        "996514ff172e71756e300a9b43fc189603d14ba914da18e5c7cf12129d014ef2",
    "phase11_policy_dataset_v1.json":
        "233e6d83a4607070d9937a3f302c27dd4a243b9373c4b692351a5f560bc3c549",
}


def assert_frozen_inputs() -> None:
    inventory = build_inventory()
    for path, digest in inventory.file_hashes:
        if SHA256.get(Path(path).name) != digest:
            raise ValueError(f"source SHA-256 changed: {path}")


def make_rankings(
    document_ids: list[str],
    document_texts: list[str],
    tasks: list[RoutingBenchmarkTask],
    document_embeddings: list[list[float]],
    query_embeddings: list[list[float]],
) -> dict[str, dict[str, list[str]]]:
    """Construct ranks with NO evaluator labels or oracle decisions."""
    if len(document_ids) != len(document_texts) or len(document_ids) != len(
        document_embeddings
    ):
        raise ValueError("document/embedding count mismatch")
    if len(tasks) != len(query_embeddings):
        raise ValueError("task/embedding count mismatch")
    if len(document_ids) != len(set(document_ids)):
        raise ValueError("duplicate document IDs")
    bm25 = BM25Retriever(document_ids, document_texts)
    rankings: dict[str, dict[str, list[str]]] = {
        "bm25": {},
        "dense": {},
        "hybrid_rrf": {},
    }
    for task, query_embedding in zip(tasks, query_embeddings):
        lexical = [
            doc_id for doc_id, _ in bm25.rank(task.question, top_k=len(document_ids))
        ]
        dense_scores = [
            (document_id, cosine_similarity(query_embedding, document_embedding))
            for document_id, document_embedding
            in zip(document_ids, document_embeddings)
        ]
        dense_scores.sort(key=lambda item: item[1], reverse=True)
        dense = [doc_id for doc_id, _ in dense_scores]
        fused = [
            doc_id
            for doc_id, _ in reciprocal_rank_fusion(
                [lexical, dense], top_k=len(document_ids), rrf_k=RRF_K
            )
        ]
        rankings["bm25"][task.task_id] = lexical
        rankings["dense"][task.task_id] = dense
        rankings["hybrid_rrf"][task.task_id] = fused
    return rankings


def main() -> None:
    # Fail before downloading model weights if source inputs have drifted.
    assert_frozen_inputs()
    documents = load_documents()
    tasks = load_tasks()
    if len(documents) != 22 or len(tasks) != 12:
        raise ValueError("unexpected frozen corpus/task size")

    # Importing/loading the encoder is kept outside pure metric/test modules.
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)
    document_ids = [doc.document_id for doc in documents]
    document_texts = [doc.text for doc in documents]
    document_embeddings = model.encode(document_texts).tolist()
    query_embeddings = model.encode([task.question for task in tasks]).tolist()
    rankings = make_rankings(
        document_ids, document_texts, tasks, document_embeddings, query_embeddings
    )
    scores = evaluate_rankings(tasks, rankings, ks=K_VALUES)
    table = aggregate(scores)
    print("Phase 13 EXP-121 — Controlled Fixed Retriever Comparison")
    print(f"model={MODEL_NAME} bm25_k1=1.5 bm25_b=0.75 rrf_k={RRF_K}")
    print(f"documents={len(documents)} tasks={len(tasks)} families={len({t.pair_id for t in tasks})}")
    print(f"k_values={K_VALUES} model_training_seeds=none bootstrap_draws=10000 bootstrap_seed=121")
    print("Frozen source hashes: verified against EXP-120.")
    print("Data status: inspected development benchmark, NOT untouched heldout.")
    print()
    print("Fixed strategies (recall, MRR, complete-gold fraction):")
    for method in ("bm25", "dense", "hybrid_rrf"):
        for k in K_VALUES:
            recall, mrr, complete = table[(method, k)]
            print(
                f"  {method:10s} K={k} recall={recall:.4f} "
                f"mrr={mrr:.4f} complete={complete:.4f}"
            )

    print()
    print("Paired FAMILY-clustered MRR@3 differences (Hybrid minus baseline):")
    for baseline in ("bm25", "dense"):
        deltas = paired_family_deltas(
            scores, better="hybrid_rrf", baseline=baseline, k=3
        )
        interval = cluster_bootstrap(deltas, draws=10_000, seed=121)
        print(
            f"  hybrid_minus_{baseline}: mean={interval.mean:+.4f} "
            f"95pct_family_bootstrap=[{interval.low:+.4f}, {interval.high:+.4f}] "
            f"families={len(deltas)}"
        )
        print(f"    family_deltas={deltas}")
    print()
    print("Limit: only six known evidence families; interval is descriptive,")
    print("not a robust population CI or independent model-seed uncertainty.")
    print("No answer generation, latency benchmarking, or learned policy evaluation.")
    print("Do not select an architecture using inspected test families and call it heldout.")


if __name__ == "__main__":
    main()
