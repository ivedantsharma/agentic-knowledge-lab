"""EXP-118: source-family-disjoint BM25 evaluation of tabular REINFORCE.

All twelve routing tasks and supporting labels originate in the real
KnowledgeBench files. Rankings are freshly computed with BM25, so they
must not be confused with the frozen hybrid Cirrus ranking of EXP-117.
The trained policy sees ONLY requested_k and steps_taken, not gold.
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean, pstdev

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.rl.reinforce import (
    TabularSoftmaxPolicy,
    evaluate_learned_policy,
    train_reinforce,
)
from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.rl.trajectory_baselines import (
    fixed_policy_actions,
    oracle_trajectory,
    score_trajectory,
)

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/phase10_routing_pairs_v0.json")
TRAIN_FAMILY = "cirrus_retry"
TRAIN_ID = "route-003"
SEEDS = (0, 1, 2, 3, 4)
GAMMA = 0.9
TRAIN_EPISODES = 1600
EVAL_EPISODES = 400


@dataclass(frozen=True)
class RankedTask:
    task_id: str
    family: str
    question: str
    ranked_ids: tuple[str, ...]
    supporting_ids: frozenset[str]
    support_rank: int


def load_ranked_tasks(
    documents_path: Path = DOCS,
    tasks_path: Path = TASKS,
) -> tuple[RankedTask, ...]:
    documents = json.loads(documents_path.read_text(encoding="utf-8"))
    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
    ids = [document["document_id"] for document in documents]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate document IDs")
    retriever = BM25Retriever(ids, [document["text"] for document in documents])
    ranked_tasks = []
    for task in tasks:
        ranking = tuple(
            document_id for document_id, _ in retriever.rank(task["question"], top_k=len(ids))
        )
        support = frozenset(task["supporting_document_ids"])
        if not support or not support.issubset(set(ranking)):
            raise ValueError("supporting documents must exist in the ranked corpus")
        rank = max(ranking.index(doc_id) + 1 for doc_id in support)
        ranked_tasks.append(
            RankedTask(
                task["task_id"],
                task["pair_id"],
                task["question"],
                ranking,
                support,
                rank,
            )
        )
    if len({task.task_id for task in ranked_tasks}) != len(ranked_tasks):
        raise ValueError("duplicate task IDs")
    return tuple(ranked_tasks)


def family_split(
    tasks: tuple[RankedTask, ...],
    *,
    train_family: str = TRAIN_FAMILY,
) -> tuple[tuple[RankedTask, ...], tuple[RankedTask, ...]]:
    train = tuple(task for task in tasks if task.family == train_family)
    heldout = tuple(task for task in tasks if task.family != train_family)
    if not train or not heldout:
        raise ValueError("train and heldout must both be nonempty")
    if {task.family for task in train} & {task.family for task in heldout}:
        raise ValueError("evidence-family leakage")
    return train, heldout


def task_kwargs(task: RankedTask) -> dict:
    """Hidden supporting IDs enter evaluation/environment only."""
    return {
        "question": task.question,
        "ranked_ids": list(task.ranked_ids),
        "supporting_ids": set(task.supporting_ids),
    }


def model_score(
    model: TabularSoftmaxPolicy,
    task: RankedTask,
    *,
    seed: int,
    episodes: int = EVAL_EPISODES,
) -> tuple[float, float, float]:
    result = evaluate_learned_policy(
        policy=model,
        **task_kwargs(task),
        conflicting_ids=set(),
        episodes=episodes,
        seed=seed,
        gamma=GAMMA,
    )
    return result.mean_discounted_return, result.completion_rate, result.mean_documents


def fixed_score(task: RankedTask, actions: tuple[RetrievalRLAction, ...]) -> tuple[float, float]:
    result = score_trajectory(
        **task_kwargs(task), conflicting_ids=set(), actions=actions, gamma=GAMMA
    )
    return result.discounted_return, result.report.coverage


def main() -> None:
    tasks = load_ranked_tasks()
    train, heldout = family_split(tasks)
    training_task = next(task for task in train if task.task_id == TRAIN_ID)
    assert training_task.family == TRAIN_FAMILY
    print("Phase 12 EXP-118 — Family-Disjoint BM25 Policy Transfer Audit")
    print("BM25 rankings RECOMPUTED for every task; distinct from EXP-117 hybrid ranking.")
    print(f"tasks={len(tasks)} train_family={TRAIN_FAMILY} train_tasks={len(train)} heldout_tasks={len(heldout)}")
    print(f"seeds={SEEDS} train_episodes={TRAIN_EPISODES} eval_episodes={EVAL_EPISODES} gamma={GAMMA}")
    print("Training on route-003 ONLY; route-004 is same-family diagnostic, not heldout.")
    print("All other families withheld from optimization and hyperparameter selection.")
    print()

    print("Actual evidence rank by task:")
    for task in tasks:
        print(
            f"  {task.task_id} family={task.family} "
            f"max_support_rank={task.support_rank} reachable_K5={task.support_rank <= 5}"
        )
    print()

    for name, actions in fixed_policy_actions().items():
        g = [fixed_score(task, actions)[0] for task in heldout]
        completion = [fixed_score(task, actions)[1] == 1 for task in heldout]
        print(
            f"heldout_fixed_{name}: mean_G={fmean(g):+.4f} "
            f"complete={fmean(completion):.4f}"
        )

    oracle_scores = [
        oracle_trajectory(**task_kwargs(task), conflicting_ids=set(), gamma=GAMMA)
        .discounted_return
        for task in heldout
    ]
    print(f"heldout_gold_oracle_mean_G={fmean(oracle_scores):+.4f}")
    print()

    before_means = []
    after_means = []
    before_completions = []
    after_completions = []
    for seed in SEEDS:
        policy = TabularSoftmaxPolicy()
        eval_seed = 5000 + seed
        before = [model_score(policy, task, seed=eval_seed) for task in heldout]
        before_train = model_score(policy, training_task, seed=eval_seed)
        training = train_reinforce(
            policy=policy,
            **task_kwargs(training_task),
            episodes=TRAIN_EPISODES,
            seed=seed,
            gamma=GAMMA,
        )
        after = [model_score(policy, task, seed=eval_seed) for task in heldout]
        after_train = model_score(policy, training_task, seed=eval_seed)
        before_g = fmean(row[0] for row in before)
        after_g = fmean(row[0] for row in after)
        before_c = fmean(row[1] for row in before)
        after_c = fmean(row[1] for row in after)
        before_means.append(before_g)
        after_means.append(after_g)
        before_completions.append(before_c)
        after_completions.append(after_c)
        print(
            f"seed={seed} training_G_before={before_train[0]:+.3f} "
            f"training_G_after={after_train[0]:+.3f} "
            f"heldout_G_before={before_g:+.3f} heldout_G_after={after_g:+.3f} "
            f"heldout_delta={after_g-before_g:+.3f} "
            f"heldout_completion_before={before_c:.3f} "
            f"heldout_completion_after={after_c:.3f} "
            f"train_last100={training.late_mean_discounted_return:+.3f}"
        )
        if seed == 0:
            print("  Seed 0 per-family heldout performance:")
            for family in sorted({task.family for task in heldout}):
                rows = [
                    model_score(policy, task, seed=eval_seed)
                    for task in heldout if task.family == family
                ]
                print(
                    f"    {family}: mean_G={fmean(row[0] for row in rows):+.3f} "
                    f"completion={fmean(row[1] for row in rows):.3f} "
                    f"docs={fmean(row[2] for row in rows):.2f}"
                )

    deltas = [after - before for before, after in zip(before_means, after_means)]
    print()
    print(
        f"heldout_mean_G_before={fmean(before_means):+.4f} "
        f"heldout_mean_G_after={fmean(after_means):+.4f} "
        f"heldout_mean_delta={fmean(deltas):+.4f} "
        f"heldout_seed_delta_sd={pstdev(deltas):.4f}"
    )
    print(
        f"heldout_mean_completion_before={fmean(before_completions):.4f} "
        f"heldout_mean_completion_after={fmean(after_completions):.4f}"
    )
    print(f"heldout_gap_to_oracle={fmean(oracle_scores)-fmean(after_means):.4f}")
    print()
    print("Interpretation: no retriever mismatch within EXP-118; family-disjoint test.")
    print("Limits: a one-family training set; no semantic policy features; only BM25.")
    print("Not comparable directly with Phase-11 hybrid-Qwen SFT accuracy.")
    print("Gold evidence coverage is not final answer correctness or conflict resolution.")


if __name__ == "__main__":
    main()
