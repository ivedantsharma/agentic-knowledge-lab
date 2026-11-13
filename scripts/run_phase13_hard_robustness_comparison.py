"""EXP-125: fixed BM25, Dense MiniLM, Hybrid risk/recall audit.

This measures retrieval and misleading source EXPOSURE. No LLM answer
generation, abstention decision or prompt-injection attack success is scored.
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.hybrid import reciprocal_rank_fusion
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document
from knowledgebench.evaluation.phase13_hard_robustness import (
    evaluate_rankings,
    summarize_cases,
)
from knowledgebench.tasks.v2_schema import KnowledgeBenchV2Task

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/knowledgebench_v2_hard_tasks_v0.json")
INJECTION_CASES = Path("data/processed/phase9_prompt_injection_pairs_v0.json")
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
K_VALUES = (1, 3, 5)


def load_inputs():
    docs = [
        KnowledgeBenchV2Document.model_validate(row)
        for row in json.loads(DOCS.read_text(encoding="utf-8"))
    ]
    tasks = [
        KnowledgeBenchV2Task.model_validate(row)
        for row in json.loads(TASKS.read_text(encoding="utf-8"))
    ]
    injections = json.loads(INJECTION_CASES.read_text(encoding="utf-8"))
    if not docs or not tasks or len({doc.document_id for doc in docs}) != len(docs):
        raise ValueError("invalid or duplicate hard-corpus documents")
    if len({task.task_id for task in tasks}) != len(tasks):
        raise ValueError("duplicate benchmark tasks")
    if not isinstance(injections, dict) or not injections.get("cases"):
        raise ValueError("missing injection case inventory")
    if len({case["case_id"] for case in injections["cases"]}) != len(injections["cases"]):
        raise ValueError("duplicate injection case")
    hashes = {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (DOCS, TASKS, INJECTION_CASES)
    }
    return docs, tasks, injections, hashes


def compute_rankings(docs, tasks, *, encoder):
    ids = [doc.document_id for doc in docs]
    texts = [doc.text for doc in docs]
    bm25 = BM25Retriever(document_ids=ids, document_texts=texts)
    embeddings = encoder.encode(texts)
    result = {"bm25": {}, "dense": {}, "hybrid_rrf": {}}
    for task in tasks:
        query = task.question
        lexical = [
            doc_id for doc_id, _ in bm25.rank(query, top_k=len(docs))
        ]
        query_vec = encoder.encode(query).tolist()
        semantic = sorted(
            (
                (doc_id, cosine_similarity(query_vec, vector.tolist()))
                for doc_id, vector in zip(ids, embeddings)
            ),
            key=lambda pair: (-pair[1], pair[0]),
        )
        dense = [doc_id for doc_id, _ in semantic]
        hybrid = [
            doc_id for doc_id, _ in reciprocal_rank_fusion(
                rankings=[lexical, dense], top_k=len(docs), rrf_k=60
            )
        ]
        result["bm25"][task.task_id] = lexical
        result["dense"][task.task_id] = dense
        result["hybrid_rrf"][task.task_id] = hybrid
    return result


def main() -> None:
    docs, tasks, injections, hashes = load_inputs()
    from sentence_transformers import SentenceTransformer

    encoder = SentenceTransformer(MODEL)
    rankings = compute_rankings(docs, tasks, encoder=encoder)
    cases = evaluate_rankings(
        tasks, rankings, document_ids={doc.document_id for doc in docs},
        k_values=K_VALUES,
    )
    summary = summarize_cases(cases)
    print("Phase 13 EXP-125 — Hard Evidence Retrieval Robustness")
    print(f"model={MODEL} documents={len(docs)} tasks={len(tasks)} k={K_VALUES}")
    print(f"phase9_existing_injection_pairs={len(injections['cases'])} (INVENTORY only)")
    for path, digest in hashes.items():
        print(f"SHA256 {path} = {digest}")
    print("Development data reused from Phase 7 and Phase 9; NOT untouched holdout.")
    print("Exposure to misleading evidence != use in an answer.")
    print("Unanswerable retrieval != failed abstention; no abstention controller.")
    print("Prompt injection attack success NOT evaluated: no clean/injected model runs.")
    for item in cases:
        print(
            f"{item.task_id} method={item.method} K={item.k} "
            f"retrieved={list(item.retrieved_ids)} "
            f"support_recall={item.support_recall} complete={item.complete_support} "
            f"risk_hits={dict(item.risk_hits)} "
            f"ambiguity_coverage={item.ambiguity_candidate_coverage}"
        )
    print("Aggregate conditional challenge diagnostics")
    for s in summary:
        print(
            f"  {s.method} K={s.k} answerable={s.answerable_count} "
            f"unanswerable={s.unanswerable_count} recall={s.mean_support_recall:.4f} "
            f"complete={s.complete_support_rate:.4f} mrr={s.mean_reciprocal_rank:.4f} "
            f"unanswerable_nonempty={s.unanswerable_nonempty_retrieval_rate:.4f} "
            f"ambiguous_n={s.ambiguity_task_count} "
            f"ambiguous_candidates_covered={s.mean_ambiguity_coverage}"
        )
        for (risk, count), (_, rate) in zip(
            s.risk_label_counts, s.conditional_risk_exposure_rates
        ):
            print(f"    {risk}_labeled_tasks={count} exposure_rate={rate}")
    print("LIMIT: no downstream answer correctness, thresholded abstention,")
    print("latency, paired prompt-injection model response, or fresh generalization.")


if __name__ == "__main__":
    main()
