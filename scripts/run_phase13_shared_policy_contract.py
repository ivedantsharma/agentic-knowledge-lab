"""EXP-124 Gate B0: run common v0 protocol with gold-blind fixed controls.

Uses exactly the existing BM25-ranked 12 Phase 10 routing tasks. Outputs are
development-baseline MECHANICS only; this runs no new SFT or RL checkpoint.
"""

import hashlib
import sys
from pathlib import Path
from statistics import fmean

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.shared_policy_protocol import (
    ACTION_NAMES,
    GAMMA,
    PROTOCOL_ID,
    FixedKPolicy,
    run_shared_episode,
)
from scripts.run_phase12_family_disjoint_transfer import (
    DOCS,
    TASKS,
    load_ranked_tasks,
)


def main() -> None:
    tasks = load_ranked_tasks()
    if len(tasks) != 12 or len({task.task_id for task in tasks}) != 12:
        raise ValueError("expected exactly twelve unique development tasks")
    print("Phase 13 EXP-124 Gate B0 — Shared Policy Execution Contract")
    print(f"protocol={PROTOCOL_ID} retriever=BM25 gamma={GAMMA}")
    print(f"actions={ACTION_NAMES}")
    print("Fixed controls only. NOT SFT inference, NOT learned RL evaluation.")
    print("Queries and source facts are previously inspected development data.")
    for path in (DOCS, TASKS):
        print(f"SHA256 {path} = {hashlib.sha256(path.read_bytes()).hexdigest()}")
    print(f"tasks={len(tasks)} families={len({task.family for task in tasks})}")
    for k in (1, 2, 3, 5):
        results = [
            run_shared_episode(
                policy=FixedKPolicy(k),
                question=task.question,
                ranked_ids=list(task.ranked_ids),
                supporting_ids=set(task.supporting_ids),
            )
            for task in tasks
        ]
        coverages = [
            len(set(result.final_observation.retrieved_ids) & task.supporting_ids)
            / len(task.supporting_ids)
            for result, task in zip(results, tasks)
        ]
        print(
            f"fixed_K{k}: mean_support_recall={fmean(coverages):.4f} "
            f"complete={fmean(x == 1.0 for x in coverages):.4f} "
            f"mean_discounted_return={fmean(r.discounted_return for r in results):+.4f} "
            f"mean_documents={fmean(r.documents_returned for r in results):.4f}"
        )
    print("PASS: one action/state/reward/STOP execution environment works.")
    print("BLOCKED: original Phase 11 SFT must be retrained for this protocol;")
    print("no new independent source families, matched checkpoints or trained")
    print("policy comparison have been supplied. EXP-124 REMAINS OPEN.")


if __name__ == "__main__":
    main()
