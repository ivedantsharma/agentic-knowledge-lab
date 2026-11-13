"""EXP-119: audit whether Phase 11 SFT labels can compare to Phase 12 RL.

This is a protocol-compatibility audit, NOT SFT inference. It never treats
hybrid retrieval supervision targets as BM25 learned-model predictions.
"""

import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.training.retrieval_policy import RetrievalPolicyAction
from scripts.run_phase12_family_disjoint_transfer import load_ranked_tasks

SFT_DATA = Path("data/processed/phase11_policy_dataset_v1.json")
BUDGETS = (1, 2, 3, 5)
SFT_TO_RL = {
    RetrievalPolicyAction.SEARCH_HYBRID_K1: RetrievalRLAction.SEARCH_K1,
    RetrievalPolicyAction.SEARCH_HYBRID_K2: RetrievalRLAction.SEARCH_K2,
    RetrievalPolicyAction.SEARCH_HYBRID_K3: RetrievalRLAction.SEARCH_K3,
    RetrievalPolicyAction.SEARCH_HYBRID_K5: RetrievalRLAction.SEARCH_K5,
}


def first_sufficient_budget(rank: int) -> int | None:
    """Minimum permitted K covering all evaluator support IDs."""
    return next((budget for budget in BUDGETS if budget >= rank), None)


def map_first_search_action(action: RetrievalPolicyAction) -> RetrievalRLAction | None:
    """Map static retrieval budget *names*, NOT retriever policies/trajectories."""
    return SFT_TO_RL.get(action)


@dataclass(frozen=True)
class SharedTaskAudit:
    task_id: str
    evidence_family_rl: str
    evidence_family_sft: str
    sft_split: str
    sft_target: RetrievalPolicyAction
    bm25_support_rank: int
    bm25_min_budget: int | None
    sft_target_budget: int | None

    @property
    def budget_matches_bm25(self) -> bool | None:
        if self.bm25_min_budget is None or self.sft_target_budget is None:
            return None
        return self.bm25_min_budget == self.sft_target_budget


def audit_shared_tasks(
    *,
    sft_path: Path = SFT_DATA,
) -> tuple[SharedTaskAudit, ...]:
    ranked = load_ranked_tasks()
    by_id = {task.task_id: task for task in ranked}
    rows = json.loads(sft_path.read_text(encoding="utf-8"))
    sft_by_id = {}
    for row in rows:
        source_id = row["source_task_id"]
        if source_id in sft_by_id:
            raise ValueError("duplicate SFT source task IDs")
        sft_by_id[source_id] = row

    audits = []
    for task in ranked:
        if task.task_id not in sft_by_id:
            continue
        sft = sft_by_id[task.task_id]
        if task.question != sft["question"]:
            raise ValueError(f"question differs across datasets: {task.task_id}")
        action = RetrievalPolicyAction(sft["target_action"])
        mapped = map_first_search_action(action)
        budget = int(mapped.value.removeprefix("SEARCH_K")) if mapped else None
        audits.append(
            SharedTaskAudit(
                task_id=task.task_id,
                evidence_family_rl=task.family,
                evidence_family_sft=sft["evidence_family"],
                sft_split=sft["split"],
                sft_target=action,
                bm25_support_rank=task.support_rank,
                bm25_min_budget=first_sufficient_budget(task.support_rank),
                sft_target_budget=budget,
            )
        )
    return tuple(audits)


def main() -> None:
    audited = audit_shared_tasks()
    sft_examples = json.loads(SFT_DATA.read_text(encoding="utf-8"))
    rl_actions = tuple(action.value for action in RetrievalRLAction)
    sft_actions = tuple(action.value for action in RetrievalPolicyAction)
    matches = [x for x in audited if x.budget_matches_bm25 is True]
    mismatches = [x for x in audited if x.budget_matches_bm25 is False]
    nonmappable = [x for x in audited if x.budget_matches_bm25 is None]
    phase11_splits = Counter(x.sft_split for x in audited)

    print("Phase 12 EXP-119 — Phase 11 / Phase 12 Protocol Compatibility Audit")
    print("No Qwen inference and no REINFORCE retraining in this experiment.")
    print(f"phase11_examples={len(sft_examples)} phase12_routing_tasks={len(load_ranked_tasks())} shared_tasks={len(audited)}")
    print(f"phase11_actions={sft_actions}")
    print(f"phase12_actions={rl_actions}")
    print("SFT REFORMULATE has no RL counterpart; RL STOP has no SFT counterpart.")
    print("Only SEARCH_HYBRID_Kn -> SEARCH_Kn budget names are syntactically mappable.")
    print("Retriever, objective, decision horizon and heldout family splits still differ.")
    print()

    for item in audited:
        print(
            f"  {item.task_id} SFT_split={item.sft_split:7s} "
            f"SFT_family={item.evidence_family_sft:16s} "
            f"RL_family={item.evidence_family_rl:16s} "
            f"SFT_target={item.sft_target.value:16s} "
            f"BM25_min_K={item.bm25_min_budget} "
            f"budget_equal={item.budget_matches_bm25}"
        )
    print()
    print(f"shared_sft_splits={dict(phase11_splits)}")
    print(
        f"budget_matches={len(matches)} budget_mismatches={len(mismatches)} "
        f"nonmappable={len(nonmappable)}"
    )
    print(
        "SFT target vs BM25 minimum-budget comparison is LABEL ALIGNMENT ONLY, "
        "not a classifier accuracy or RL return metric."
    )
    print("Phase-11 SFT heldout Meridian is inside EXP-118 RL heldout, but")
    print("Borealis is Phase-11 dev, and Nimbus/Orion/Solstice are Phase-11 train.")
    print("Therefore the EXP-118 ten-task heldout metric is NOT a Phase-11 heldout metric.")
    print("Conclusion: direct Phase-11 LoRA-vs-Phase-12 RL performance claims are invalid.")
    print("Future comparison requires common retriever, action space, train split,")
    print("terminal protocol, inference checkpoints and evaluation metric.")


if __name__ == "__main__":
    main()
