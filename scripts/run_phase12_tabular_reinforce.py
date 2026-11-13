"""EXP-117: first true policy-gradient update, deliberately in-sample only.

No Qwen/LoRA training here. Train one tabular policy on the grounded
Cirrus route-003 environment and measure multiple random seeds.
"""

import json
import sys
from pathlib import Path
from statistics import fmean, pstdev

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.reinforce import (
    TabularSoftmaxPolicy,
    evaluate_learned_policy,
    train_reinforce,
)
from knowledge_engine.rl.retrieval_environment import RetrievalEpisodeV2, RetrievalRLAction
from knowledge_engine.rl.stochastic_policy import StochasticBudgetPolicy, evaluate_policy
from knowledge_engine.rl.trajectory_baselines import oracle_trajectory, score_trajectory
from scripts.run_phase12_reward_v2_trajectory_sweep import RANKING, cases

DOCUMENTS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/phase10_routing_pairs_v0.json")
TRAIN_EPISODES = 2500
EVAL_EPISODES = 800
SEEDS = (0, 1, 2, 3, 4)
GAMMA = 0.9


def main() -> None:
    documents = json.loads(DOCUMENTS.read_text(encoding="utf-8"))
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))
    by_id = {doc["document_id"]: doc for doc in documents}
    task = next(item for item in tasks if item["task_id"] == "route-003")
    assert set(RANKING).issubset(by_id)
    assert by_id[RANKING[0]]["source_type"] == "pending_policy_revision"
    assert by_id[RANKING[1]]["source_type"] == "service_manual"
    assert set(task["supporting_document_ids"]) == {RANKING[1]}

    question = task["question"]
    support = set(task["supporting_document_ids"])
    kwargs = {
        "question": question,
        "ranked_ids": list(RANKING),
        "supporting_ids": support,
        "conflicting_ids": {RANKING[0]},
    }
    oracle = oracle_trajectory(**kwargs, gamma=GAMMA)
    fixed = score_trajectory(
        **kwargs,
        actions=(RetrievalRLAction.SEARCH_K2, RetrievalRLAction.STOP),
        gamma=GAMMA,
    )
    eps_k2 = evaluate_policy(
        **kwargs,
        policy=StochasticBudgetPolicy(RetrievalRLAction.SEARCH_K2, epsilon=0.2),
        episodes=EVAL_EPISODES,
        seed=4000,
        gamma=GAMMA,
    )

    print("Phase 12 EXP-117 — Tabular REINFORCE Policy Gradient")
    print("Training/evaluation on the SAME grounded Cirrus query: mechanics, not generalization.")
    print(f"train_episodes={TRAIN_EPISODES} eval_episodes={EVAL_EPISODES}")
    print(f"seeds={SEEDS} gamma={GAMMA} learning_rate=0.08 baseline_rate=0.05")
    print("Policy inputs: requested_k and steps_taken only; rewards from hidden evaluator gold.")
    print(f"gold_oracle_G={oracle.discounted_return:+.4f}")
    print(f"fixed_K2_G={fixed.discounted_return:+.4f}")
    print(f"EXP116_epsilon_K2_G={eps_k2.mean_discounted_return:+.4f}")
    print()

    before_values = []
    after_values = []
    trained_models: dict[int, TabularSoftmaxPolicy] = {}
    for seed in SEEDS:
        model = TabularSoftmaxPolicy()
        eval_seed = 4000 + seed
        before = evaluate_learned_policy(
            **kwargs, policy=model, episodes=EVAL_EPISODES, seed=eval_seed, gamma=GAMMA
        )
        training = train_reinforce(
            policy=model,
            question=question,
            ranked_ids=list(RANKING),
            supporting_ids=support,
            episodes=TRAIN_EPISODES,
            seed=seed,
            gamma=GAMMA,
        )
        after = evaluate_learned_policy(
            **kwargs, policy=model, episodes=EVAL_EPISODES, seed=eval_seed, gamma=GAMMA
        )
        initial_observation = RetrievalEpisodeV2(
            question, list(RANKING), support
        ).observe()
        k2_probability = model.probabilities(initial_observation)[RetrievalRLAction.SEARCH_K2]
        before_values.append(before.mean_discounted_return)
        after_values.append(after.mean_discounted_return)
        trained_models[seed] = model
        print(
            f"seed={seed} G_before={before.mean_discounted_return:+.3f} "
            f"G_after={after.mean_discounted_return:+.3f} "
            f"delta={after.mean_discounted_return-before.mean_discounted_return:+.3f} "
            f"train_first100={training.early_mean_discounted_return:+.3f} "
            f"train_last100={training.late_mean_discounted_return:+.3f} "
            f"complete_before={before.completion_rate:.3f} "
            f"complete_after={after.completion_rate:.3f} "
            f"docs_after={after.mean_documents:.2f} "
            f"premature_STOP_after={after.premature_stop_rate:.3f} "
            f"timeout_after={after.timeout_rate:.3f} "
            f"P_initial_K2={k2_probability:.3f}"
        )
    deltas = [after - before for after, before in zip(after_values, before_values)]
    print()
    print(
        f"mean_before={fmean(before_values):+.4f} "
        f"mean_after={fmean(after_values):+.4f} "
        f"mean_delta={fmean(deltas):+.4f} "
        f"sd_delta_across_seeds={pstdev(deltas):.4f}"
    )
    print(f"oracle_gap_after={oracle.discounted_return-fmean(after_values):.4f}")

    # Negative control: sampling without gradient updates is not learning.
    control = TabularSoftmaxPolicy()
    before_control = evaluate_learned_policy(
        **kwargs, policy=control, episodes=EVAL_EPISODES, seed=4000, gamma=GAMMA
    )
    train_reinforce(
        policy=control,
        question=question,
        ranked_ids=list(RANKING),
        supporting_ids=support,
        episodes=TRAIN_EPISODES,
        seed=0,
        learning_rate=0.0,
        gamma=GAMMA,
    )
    after_control = evaluate_learned_policy(
        **kwargs, policy=control, episodes=EVAL_EPISODES, seed=4000, gamma=GAMMA
    )
    assert after_control.mean_discounted_return == before_control.mean_discounted_return
    print(f"zero_learning_rate_control_delta={after_control.mean_discounted_return-before_control.mean_discounted_return:+.4f}")

    print()
    print("Post-training transfer probes: SYNTHETIC, not held-out real tasks.")
    for case in cases(question, frozenset(support)):
        if not case.synthetic:
            continue
        probe = evaluate_learned_policy(
            policy=trained_models[0],
            question=case.question,
            ranked_ids=list(case.ranked_ids),
            supporting_ids=set(case.supporting_ids),
            conflicting_ids=set(case.conflicting_ids),
            episodes=EVAL_EPISODES,
            seed=4000,
            gamma=GAMMA,
        )
        print(
            f"  {case.name}: G={probe.mean_discounted_return:+.3f} "
            f"coverage={probe.mean_coverage:.3f} complete={probe.completion_rate:.3f}"
        )

    print()
    print("Interpretation: this is real REINFORCE on one frozen question.")
    print("Caution: increased training-task reward is NOT heldout knowledge generalization.")
    print("Caution: evidence coverage remains a proxy; no answer-quality or safety claim.")


if __name__ == "__main__":
    main()
