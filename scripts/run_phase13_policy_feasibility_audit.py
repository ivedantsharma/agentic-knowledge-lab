"""EXP-124 Gate A: policy-protocol feasibility, NOT model inference.

Uses actual current training/RL action enums, SFT data, and existing
EXP-119 cross-task audit. Never treats label matches as learned predictions.
"""

import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.rl.retrieval_environment import RetrievalRLAction
from knowledge_engine.training.retrieval_policy import RetrievalPolicyAction
from scripts.run_phase12_policy_protocol_audit import (
    SFT_DATA,
    audit_shared_tasks,
)

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
ROUTES = Path("data/processed/phase10_routing_pairs_v0.json")
SFT_SCRIPT = Path("scripts/run_phase11_class_balanced_lora_sft.py")
RL_SCRIPT = Path("scripts/run_phase12_family_disjoint_transfer.py")


@dataclass(frozen=True)
class ProtocolFeasibility:
    hashes: tuple[tuple[str, str], ...]
    sft_actions: tuple[str, ...]
    rl_actions: tuple[str, ...]
    split_sizes: tuple[tuple[str, int], ...]
    route_count: int
    shared_route_tasks: int
    budget_label_matches: int
    budget_label_mismatches: int
    budget_label_unmappable: int
    sft_family_splits: tuple[tuple[str, str], ...]
    identical_action_space: bool
    shared_retriever: bool
    shared_terminal_protocol: bool
    same_heldout_split: bool
    independent_new_families_present: bool
    training_scripts_persist_checkpoints: bool

    @property
    def ready_for_direct_learned_comparison(self) -> bool:
        return all((
            self.identical_action_space, self.shared_retriever,
            self.shared_terminal_protocol, self.same_heldout_split,
            self.independent_new_families_present,
            self.training_scripts_persist_checkpoints,
        ))


def audit_policy_feasibility(
    *,
    sft_path: Path = SFT_DATA,
    routes_path: Path = ROUTES,
    docs_path: Path = DOCS,
    sft_script_path: Path = SFT_SCRIPT,
    rl_script_path: Path = RL_SCRIPT,
) -> ProtocolFeasibility:
    files = (docs_path, routes_path, sft_path, sft_script_path, rl_script_path)
    hashes = tuple((str(path), hashlib.sha256(path.read_bytes()).hexdigest())
                   for path in files)
    rows = json.loads(sft_path.read_text(encoding="utf-8"))
    routes = json.loads(routes_path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("missing SFT examples")
    if not isinstance(routes, list) or not routes:
        raise ValueError("missing routing tasks")
    if len({row["source_task_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate supervised task IDs")
    if len({route["task_id"] for route in routes}) != len(routes):
        raise ValueError("duplicate routing task IDs")
    split_sizes = Counter(row["split"] for row in rows)
    if set(split_sizes) != {"train", "dev", "heldout"}:
        raise ValueError("unexpected supervised splits")
    families: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row["target_action"] not in {action.value for action in RetrievalPolicyAction}:
            raise ValueError("unknown SFT action")
        families[row["evidence_family"]].add(row["split"])
    if any(len(splits) > 1 for splits in families.values()):
        raise ValueError("SFT family used across train/dev/heldout")
    audited = audit_shared_tasks(sft_path=sft_path)
    matches = sum(row.budget_matches_bm25 is True for row in audited)
    mismatches = sum(row.budget_matches_bm25 is False for row in audited)
    unmappable = sum(row.budget_matches_bm25 is None for row in audited)
    # These are source-level and protocol facts, not assumptions that the
    # local user environment contains no model checkpoint.
    sft_code = sft_script_path.read_text(encoding="utf-8")
    rl_code = rl_script_path.read_text(encoding="utf-8")
    persists = (
        "save_pretrained(" in sft_code
        and ("torch.save(" in rl_code or "pickle.dump(" in rl_code)
    )
    sft_actions = tuple(action.value for action in RetrievalPolicyAction)
    rl_actions = tuple(action.value for action in RetrievalRLAction)
    # Existing experiments use different retrievers, terminal conventions,
    # heldout evaluation groups, and already inspected source families.
    return ProtocolFeasibility(
        hashes=hashes,
        sft_actions=sft_actions,
        rl_actions=rl_actions,
        split_sizes=tuple(sorted(split_sizes.items())),
        route_count=len(routes),
        shared_route_tasks=len(audited),
        budget_label_matches=matches,
        budget_label_mismatches=mismatches,
        budget_label_unmappable=unmappable,
        sft_family_splits=tuple(sorted((family, next(iter(splits)))
                                       for family, splits in families.items())),
        identical_action_space=set(sft_actions) == set(rl_actions),
        shared_retriever=False,
        shared_terminal_protocol=False,
        same_heldout_split=False,
        independent_new_families_present=False,
        training_scripts_persist_checkpoints=persists,
    )


def main() -> None:
    result = audit_policy_feasibility()
    print("Phase 13 EXP-124 Gate A — Learned Policy Comparison Feasibility")
    print("No trained model inference or fresh evaluation families in this audit.")
    for path, digest in result.hashes:
        print(f"SHA256 {path} = {digest}")
    print(f"sft_actions={result.sft_actions}")
    print(f"rl_actions={result.rl_actions}")
    print(f"sft_splits={dict(result.split_sizes)}")
    print(f"sft_family_splits={dict(result.sft_family_splits)}")
    print(
        f"routes={result.route_count} shared_route_tasks={result.shared_route_tasks} "
        f"label_matches={result.budget_label_matches} "
        f"label_mismatches={result.budget_label_mismatches} "
        f"label_unmappable={result.budget_label_unmappable}"
    )
    for key in (
        "identical_action_space", "shared_retriever",
        "shared_terminal_protocol", "same_heldout_split",
        "independent_new_families_present", "training_scripts_persist_checkpoints",
    ):
        print(f"{key}={getattr(result, key)}")
    print(f"ready_for_direct_learned_comparison={result.ready_for_direct_learned_comparison}")
    if not result.ready_for_direct_learned_comparison:
        print("BLOCKED: previous SFT classification and RL return are not")
        print("comparable learned-policy outcomes. No superiority claim permitted.")
        print("Training scripts' checkpoint persistence check is source-only;")
        print("it does not determine files in the user's unconnected workspace.")
    print("Next: freeze common inference/action/retriever protocol, independently")
    print("source evaluation families, and save actual model checkpoints.")


if __name__ == "__main__":
    main()
