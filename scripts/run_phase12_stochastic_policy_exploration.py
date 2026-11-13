"""EXP-116: reproducible stochastic retrieval-policy exploration (NO training).

Grounded Cirrus route-003 uses actual gold. Other configurations use
synthetically changed supporting IDs to stress reward mechanics only.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.rl.stochastic_policy import StochasticBudgetPolicy, evaluate_policy
from knowledge_engine.rl.trajectory_baselines import oracle_trajectory
from scripts.run_phase12_reward_v2_trajectory_sweep import RANKING, cases

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/phase10_routing_pairs_v0.json")
EPISODES = 400
SEED = 116
GAMMA = 0.9
POLICIES = {
    "UNIFORM": StochasticBudgetPolicy(target=RetrievalRLAction.STOP, epsilon=1.0),
    "EPS_K2": StochasticBudgetPolicy(target=RetrievalRLAction.SEARCH_K2, epsilon=0.2),
    "EPS_K5": StochasticBudgetPolicy(target=RetrievalRLAction.SEARCH_K5, epsilon=0.2),
}


def main() -> None:
    documents = json.loads(DOCS.read_text(encoding="utf-8"))
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))
    documents_by_id = {item["document_id"]: item for item in documents}
    task = next(item for item in tasks if item["task_id"] == "route-003")
    assert set(RANKING).issubset(documents_by_id)
    assert documents_by_id[RANKING[0]]["source_type"] == "pending_policy_revision"
    assert documents_by_id[RANKING[1]]["source_type"] == "service_manual"
    assert set(task["supporting_document_ids"]) == {RANKING[1]}

    print("Phase 12 EXP-116 — Stochastic Policy Exploration (NO training)")
    print(f"episodes_per_configuration={EPISODES} seed={SEED} gamma={GAMMA}")
    print("Action masking uses observation.requested_k; hidden labels are evaluator-only.")
    print("max_steps=6 cannot time out under the strictly increasing legal action set.")
    print("max_steps=2 makes timeout possible, testing the repair in actual rollouts.")
    print()

    for case in cases(task["question"], frozenset(task["supporting_document_ids"])):
        kwargs = {
            "question": case.question,
            "ranked_ids": list(case.ranked_ids),
            "supporting_ids": set(case.supporting_ids),
            "conflicting_ids": set(case.conflicting_ids),
        }
        print(f"{case.name} ({'synthetic' if case.synthetic else 'grounded'})")
        for cap in (2, 6):
            oracle = oracle_trajectory(**kwargs, gamma=GAMMA, max_steps=cap)
            print(
                f"  cap={cap} gold_oracle_G={oracle.discounted_return:+.3f} "
                f"actions={[action.value for action in oracle.actions]}"
            )
            for name, policy in POLICIES.items():
                report = evaluate_policy(
                    **kwargs,
                    policy=policy,
                    episodes=EPISODES,
                    seed=SEED,
                    gamma=GAMMA,
                    max_steps=cap,
                )
                gap = oracle.discounted_return - report.mean_discounted_return
                assert gap >= -1e-9
                print(
                    f"    {name:7s} G={report.mean_discounted_return:+.3f} "
                    f"gap={gap:.3f} std_return={report.return_std:.3f} "
                    f"coverage={report.mean_coverage:.3f} "
                    f"complete={report.completion_rate:.3f} "
                    f"early_STOP={report.premature_stop_rate:.3f} "
                    f"timeout={report.timeout_rate:.3f} "
                    f"docs={report.mean_documents:.2f} "
                    f"conflict_exposure={report.mean_conflicting_exposure:.2f} "
                    f"unique_paths={report.unique_trajectories}"
                )
        print()

    print("Interpretation: epsilon randomizes legal actions, it does not learn a policy.")
    print("Reward gaps are against a hidden-label diagnostic upper bound.")
    print("Limits: frozen ranking; three stress cases synthetic; no answer correctness metric.")
    print("Next: controlled policy-gradient training only after this exploration baseline.")


if __name__ == "__main__":
    main()
