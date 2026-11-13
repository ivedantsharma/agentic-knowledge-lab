import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.rl.reward_audit import audit_trajectory

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/phase10_routing_pairs_v0.json")
RANKING = [
    "kbv2-doc-cirrus-contradiction",
    "kbv2-doc-cirrus-manual",
    "kbv2-doc-cumulus-retry",
    "kbv2-doc-cirrus-org",
    "kbv2-doc-borealis-stale",
]


def main() -> None:
    documents = json.loads(DOCS.read_text(encoding="utf-8"))
    document_by_id = {doc["document_id"]: doc for doc in documents}
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))
    task = next(task for task in tasks if task["task_id"] == "route-003")
    assert set(RANKING).issubset(document_by_id)
    assert document_by_id[RANKING[0]]["source_type"] == "pending_policy_revision"

    print("Phase 12 EXP-113 — Reward v2 Timeout Repair")
    print("Same frozen Cirrus ranking as EXP-111/112")
    print()

    scenarios = [
        (
            "incomplete timeout",
            [RetrievalRLAction.SEARCH_K1],
            1,
        ),
        (
            "premature STOP",
            [RetrievalRLAction.SEARCH_K1, RetrievalRLAction.STOP],
            6,
        ),
        (
            "complete STOP",
            [
                RetrievalRLAction.SEARCH_K1,
                RetrievalRLAction.SEARCH_K2,
                RetrievalRLAction.STOP,
            ],
            6,
        ),
        (
            "complete timeout",
            [RetrievalRLAction.SEARCH_K2],
            1,
        ),
    ]

    for name, actions, max_steps in scenarios:
        print(name)
        for version in ("v1", "v2"):
            report, transitions = audit_trajectory(
                question=task["question"],
                ranked_ids=RANKING,
                supporting_ids=set(task["supporting_document_ids"]),
                conflicting_ids={RANKING[0]},
                actions=actions,
                max_steps=max_steps,
                reward_version=version,
            )
            print(
                f"  {version}: "
                f"rewards={[round(t.reward, 2) for t in transitions]} "
                f"return={report.total_reward:+.2f} "
                f"coverage={report.coverage:.1f} "
                f"conflict_exposure={report.conflicting_exposure_count} "
                f"timeout={report.terminal_without_stop}"
            )
        print()

    print("Expected: incomplete timeout v2 equals explicit early STOP.")
    print("Complete trajectories unchanged; conflict exposure remains diagnostic.")


if __name__ == "__main__":
    main()
