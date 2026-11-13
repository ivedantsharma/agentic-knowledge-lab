import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.rl.reward_audit import audit_trajectory


DOCUMENTS_PATH = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS_PATH = Path("data/processed/phase10_routing_pairs_v0.json")

# Frozen top-five ranking observed in EXP-111. Do not quietly recompute it:
# this audit tests reward mechanics, not retrieval ranking/model drift.
RANKING = [
    "kbv2-doc-cirrus-contradiction",
    "kbv2-doc-cirrus-manual",
    "kbv2-doc-cumulus-retry",
    "kbv2-doc-cirrus-org",
    "kbv2-doc-borealis-stale",
]


def show(name: str, **kwargs: object) -> None:
    report, transitions = audit_trajectory(**kwargs)
    print(name)
    print(f"  actions={[t.action.value for t in transitions]}")
    print(f"  rewards={[round(t.reward, 2) for t in transitions]}")
    print(f"  total_reward={report.total_reward:.2f}")
    print(f"  evidence_coverage={report.coverage:.4f}")
    print(f"  retrieved_document_count={report.retrieval_cost_count}")
    print(f"  conflicting_exposure_count={report.conflicting_exposure_count}")
    print(f"  stopped_explicitly={report.stopped_explicitly}")
    print(f"  terminal_without_stop={report.terminal_without_stop}")
    print()


def main() -> None:
    documents = json.loads(DOCUMENTS_PATH.read_text(encoding="utf-8"))
    documents_by_id = {document["document_id"]: document for document in documents}
    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    task = next(item for item in tasks if item["task_id"] == "route-003")
    assert set(RANKING).issubset(documents_by_id)
    assert documents_by_id[RANKING[0]]["source_type"] == "pending_policy_revision"
    assert documents_by_id[RANKING[1]]["source_type"] == "service_manual"
    supporting_ids = set(task["supporting_document_ids"])
    conflicting_ids = {RANKING[0]}
    print("Phase 12 EXP-112 — Reward Validity and Termination Audit")
    print("Ranking frozen from EXP-111; gold/conflict IDs used only for audit.")
    print("Conflicting exposure is NOT proven answer contamination.")
    print()

    common = {
        "question": task["question"],
        "ranked_ids": RANKING,
        "supporting_ids": supporting_ids,
        "conflicting_ids": conflicting_ids,
    }
    show(
        "A: stop early",
        **common,
        actions=[RetrievalRLAction.SEARCH_K1, RetrievalRLAction.STOP],
    )
    show(
        "B: retrieve supporting and conflicting evidence, then stop",
        **common,
        actions=[
            RetrievalRLAction.SEARCH_K1,
            RetrievalRLAction.SEARCH_K2,
            RetrievalRLAction.STOP,
        ],
    )
    show(
        "C: force time limit without STOP (demonstrates missing terminal penalty)",
        **common,
        actions=[RetrievalRLAction.SEARCH_K1],
        max_steps=1,
    )
    show(
        "D: same initial search and early stop with normal limit",
        **common,
        actions=[RetrievalRLAction.SEARCH_K1, RetrievalRLAction.STOP],
    )
    print("Interpretation: v1 reward measures coverage/cost but ignores conflict")
    print("and omits an incomplete-episode penalty when max_steps expires.")


if __name__ == "__main__":
    main()
