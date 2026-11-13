"""EXP-123: compare static dense retrieval with evidence-conditioned searches.

User-facing driver: pretrained MiniLM is loaded only here, not in unit tests.
The historic Phase 4 data are exposed development cases, NOT new heldout.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.search_tool import DenseSearchTool
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.evaluation.phase13_static_agentic_comparison import (
    ARM_NAMES,
    aggregate_grades,
    grade_traces,
    run_arm,
)
from knowledgebench.tasks.multihop_loader import load_multihop_tasks_json

DOCUMENTS_PATH = Path("data/processed/phase4_ood_corpus_v0.jsonl")
TASKS_PATH = Path("data/processed/phase4_planner_benchmark_v0.json")
MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_and_validate_inputs():
    documents = load_documents_jsonl(DOCUMENTS_PATH)
    tasks = load_multihop_tasks_json(TASKS_PATH)
    document_ids = {doc.document_id for doc in documents}
    if not documents or not tasks:
        raise ValueError("empty experiment source")
    if len({task.task_id for task in tasks}) != len(tasks):
        raise ValueError("duplicate benchmark task ID")
    for task in tasks:
        if not task.hops:
            raise ValueError(f"missing expected evidence chain: {task.task_id}")
        if any(hop.expected_document_id not in document_ids for hop in task.hops):
            raise ValueError(f"gold evidence document missing: {task.task_id}")
    hashes = {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (DOCUMENTS_PATH, TASKS_PATH)
    }
    return documents, tasks, hashes


def main() -> None:
    documents, tasks, hashes = load_and_validate_inputs()
    from sentence_transformers import SentenceTransformer

    encoder = SentenceTransformer(MODEL)
    backend = DenseSearchTool(documents, MODEL, model=encoder)
    text_by_id = {doc.document_id: doc.text for doc in documents}
    traces = [
        run_arm(
            question=task.question, task_id=task.task_id,
            arm=arm, backend=backend, document_texts=text_by_id,
        )
        for task in tasks for arm in ARM_NAMES
    ]
    scores = grade_traces(tasks, traces)
    summary = aggregate_grades(scores)

    print("Phase 13 EXP-123 — Static versus multi-step evidence search")
    print(f"encoder={MODEL} corpus_documents={len(documents)} tasks={len(tasks)}")
    print("Shared backend: DenseSearchTool, same encoder and source documents.")
    for path, digest in hashes.items():
        print(f"SHA256 {path} = {digest}")
    print("Arms: static top3 (1 call), static top9 (1 call),")
    print("static repeated top3 (3 calls), rule planner (max 3 calls).")
    print("Top3 per planner call, planner sees only top1 observation.")
    print("All returned IDs from all calls count for EVIDENCE coverage.")
    print("No matched answer generator. NO comparative answer accuracy reported.")
    print("Existing inspected Phase 4 benchmark; NOT independent heldout.")
    for task in tasks:
        print(f"{task.task_id}: required_hops={len(task.hops)}")
        for score in scores:
            if score.task_id == task.task_id:
                trace = next(
                    t for t in traces
                    if t.task_id == task.task_id and t.arm == score.arm
                )
                print(
                    f"  {score.arm}: recall={score.recall:.4f} "
                    f"complete={score.complete} calls={score.calls} "
                    f"unique_docs={score.unique_docs} repeated={score.repeated_queries} "
                    f"stopped={score.stopped} failed={score.planner_failed}"
                )
                print(f"    queries={list(trace.queries)}")
                print(f"    observed_top1={list(trace.observed_top1)}")
                print(f"    retrieved_by_call={[list(ids) for ids in trace.retrieved_per_call]}")
    print("Aggregates")
    for arm, result in summary.items():
        print(
            f"  {arm}: "
            + " ".join(f"{key}={value:.4f}" for key, value in result.items())
        )
    print("Interpretation: top9 vs 3x top3 matches maximum exposed hit slots,")
    print("not search calls or query-adaptation cost. Repeated top3 matches")
    print("agent call ceiling but not distinct evidence opportunity.")
    print("No model finetuning, wall-clock latency or unseen-family inference.")


if __name__ == "__main__":
    main()
