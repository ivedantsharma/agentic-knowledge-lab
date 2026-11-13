"""EXP-115 — finite-horizon returns and gold-only diagnostic policy ceiling.

The actual route-003 labels remain grounded; changed-support stress cases
are synthetic and must NOT be presented as benchmark performance.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.trajectory_baselines import (
    fixed_policy_actions,
    legal_terminated_trajectories,
    oracle_trajectory,
    score_trajectory,
)
from scripts.run_phase12_reward_v2_trajectory_sweep import RANKING, cases

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/phase10_routing_pairs_v0.json")


def main() -> None:
    docs = json.loads(DOCS.read_text(encoding="utf-8"))
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))
    by_id = {doc["document_id"]: doc for doc in docs}
    task = next(row for row in tasks if row["task_id"] == "route-003")
    assert set(RANKING).issubset(by_id)
    assert by_id[RANKING[0]]["source_type"] == "pending_policy_revision"
    assert by_id[RANKING[1]]["source_type"] == "service_manual"
    assert set(task["supporting_document_ids"]) == {RANKING[1]}

    print("Phase 12 EXP-115 — Return, Discount & Finite-Horizon Oracle")
    print("Same frozen Cirrus ranking; synthetic stress cases marked.")
    print("Oracle sees gold labels ONLY for evaluation; fixed policies do not.")
    print(f"legal_terminal_trajectories={len(legal_terminated_trajectories())}")
    print()

    for case in cases(task["question"], frozenset(task["supporting_document_ids"])):
        kwargs = {
            "question": case.question,
            "ranked_ids": list(case.ranked_ids),
            "supporting_ids": set(case.supporting_ids),
            "conflicting_ids": set(case.conflicting_ids),
        }
        print(f"{case.name} ({'synthetic' if case.synthetic else 'grounded'})")
        for gamma in (1.0, 0.9):
            oracle = oracle_trajectory(**kwargs, gamma=gamma)
            print(
                f"  gold_oracle gamma={gamma:.1f} "
                f"actions={[action.value for action in oracle.actions]} "
                f"G0={oracle.discounted_return:+.4f} "
                f"coverage={oracle.report.coverage:.2f} "
                f"docs={oracle.report.retrieval_cost_count}"
            )
        for name, actions in fixed_policy_actions().items():
            result = score_trajectory(**kwargs, actions=actions)
            print(
                f"  {name:9s} return={result.report.total_reward:+.2f} "
                f"coverage={result.report.coverage:.2f} "
                f"docs={result.report.retrieval_cost_count}"
            )
        print()

    print("Interpretation: gamma=1 can tie staged and direct top-K retrieval.")
    print("gamma<1 changes credit assignment; gold-aware oracles are upper bounds.")
    print("Limit: evidence coverage is not answer correctness or contradiction resolution.")
    print("Limit: frozen/synthetic cases cannot establish heldout policy generalization.")


if __name__ == "__main__":
    main()
