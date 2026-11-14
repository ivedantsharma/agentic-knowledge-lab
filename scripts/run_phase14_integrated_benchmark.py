"""Phase 14 integrated KnowledgeBench diagnostic on previously inspected tasks.

Gold questions/support/answers are used ONLY AFTER the engine and extractor
return their outputs. This is a development diagnostic, not fresh holdout.
"""

import hashlib
import json
import sys
from pathlib import Path
from statistics import fmean

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.integrated.verification import extract_source_answer
from knowledgebench.evaluation.short_answer_equivalence import short_answers_equivalent
from knowledgebench.tasks.v2_schema import KnowledgeBenchV2Task
from scripts.run_phase14_integrated_demo import DOCUMENTS, build_engine

TASKS = Path("data/processed/knowledgebench_v2_hard_tasks_v0.json")


def evaluate_development_tasks():
    engine = build_engine()
    tasks = [
        KnowledgeBenchV2Task.model_validate(item)
        for item in json.loads(TASKS.read_text(encoding="utf-8"))
    ]
    if not tasks or len({task.task_id for task in tasks}) != len(tasks):
        raise ValueError("invalid benchmark task IDs")
    reports = []
    for strategy in ("static", "auto"):
        for task in tasks:
            result = engine.query(task.question, strategy=strategy, top_k=3)
            verdict = extract_source_answer(result)
            ids = {hit.document_id for hit in result.evidence}
            support = task.supporting_document_ids
            reports.append({
                "strategy": strategy,
                "task_id": task.task_id,
                "should_answer": task.should_answer,
                "retrieved_count": len(ids),
                "steps": len(result.steps),
                "fallback": result.fallback_reason,
                "retrieval_recall": len(ids & support) / len(support) if support else None,
                "complete_support": support.issubset(ids) if support else None,
                "source_answer_status": verdict.status,
                "source_answer": verdict.answer,
                "citation_ids": list(verdict.citation_document_ids),
                "answer_correct": (
                    short_answers_equivalent(verdict.answer, task.expected_answer)
                    if task.should_answer else None
                ),
                "abstained": verdict.answer is None,
                "unanswerable_abstained": (
                    verdict.answer is None if not task.should_answer else None
                ),
            })
    return reports


def summarize(reports):
    if not reports:
        raise ValueError("missing reports")
    summary = {}
    for strategy in ("static", "auto"):
        rows = [row for row in reports if row["strategy"] == strategy]
        ans = [row for row in rows if row["should_answer"]]
        unans = [row for row in rows if not row["should_answer"]]
        if not ans or not unans:
            raise ValueError("expected both answerable and unanswerable tasks")
        summary[strategy] = {
            "answerable_count": len(ans),
            "unanswerable_count": len(unans),
            "mean_evidence_recall": fmean(row["retrieval_recall"] for row in ans),
            "complete_support_rate": fmean(float(row["complete_support"]) for row in ans),
            "extractive_answer_accuracy_on_answerable": fmean(
                float(row["answer_correct"]) for row in ans
            ),
            "answerable_abstention_rate": fmean(float(row["abstained"]) for row in ans),
            "unanswerable_abstention_rate": fmean(
                float(row["unanswerable_abstained"]) for row in unans
            ),
            "mean_unique_docs": fmean(row["retrieved_count"] for row in rows),
            "mean_search_calls": fmean(row["steps"] for row in rows),
            "fallback_rate": fmean(float(row["fallback"] is not None) for row in rows),
        }
    return summary


def main() -> None:
    reports = evaluate_development_tasks()
    summary = summarize(reports)
    print("Phase 14 — Integrated retrieval + narrow source-supported extractor")
    print("This is an INSPECTED DEVELOPMENT benchmark, not a clean holdout.")
    print("The extractor is narrowly templated and NOT a general fact checker.")
    print("Static top3 vs planner/auto up to 3 top3 + fallback: UNMATCHED budgets.")
    for path in (DOCUMENTS, TASKS):
        print(f"SHA256 {path} = {hashlib.sha256(path.read_bytes()).hexdigest()}")
    print(f"tasks={len(reports) // 2} arms=static,auto")
    for report in reports:
        print(json.dumps(report, sort_keys=True))
    for strategy, data in summary.items():
        print(f"{strategy}: " + " ".join(
            f"{key}={value:.4f}" if isinstance(value, float) else f"{key}={value}"
            for key, value in data.items()
        ))
    print("WARNING: source-supported answer accuracy here is NOT independently")
    print("verified world truth; abstention rate on four old tasks is NOT")
    print("calibrated generalization. No SFT/RL or prompt-injection model evaluated.")


if __name__ == "__main__":
    main()
