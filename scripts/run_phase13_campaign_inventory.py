"""EXP-120: deterministic provenance and split audit for Phase 13 inputs.

Reads the existing benchmark datasets without creating labels or running
a policy. Source hashes refer to exact file bytes for reproducibility.
"""

import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
ROUTES = Path("data/processed/phase10_routing_pairs_v0.json")
POLICIES = Path("data/processed/phase11_policy_dataset_v1.json")
PREVIOUS_RL_TRAIN_FAMILY = "cirrus_retry"


@dataclass(frozen=True)
class CampaignInventory:
    file_hashes: tuple[tuple[str, str], ...]
    document_count: int
    route_count: int
    policy_example_count: int
    route_families: tuple[str, ...]
    route_family_counts: tuple[tuple[str, int], ...]
    policy_split_counts: tuple[tuple[str, int], ...]
    route_sft_split_by_family: tuple[tuple[str, str], ...]
    previously_inspected_families: tuple[str, ...]


def _read_json_list(path: Path) -> tuple[list[dict], str]:
    content = path.read_bytes()
    result = json.loads(content)
    if not isinstance(result, list):
        raise TypeError(f"expected top-level JSON list: {path}")
    return result, hashlib.sha256(content).hexdigest()


def _unique_ids(rows: list[dict], field: str) -> set[str]:
    values = [row[field] for row in rows]
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {field} found")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(f"blank or invalid {field} found")
    return set(values)


def build_inventory(
    docs_path: Path = DOCS,
    routes_path: Path = ROUTES,
    policies_path: Path = POLICIES,
) -> CampaignInventory:
    documents, docs_sha = _read_json_list(docs_path)
    routes, routes_sha = _read_json_list(routes_path)
    policies, policies_sha = _read_json_list(policies_path)

    doc_ids = _unique_ids(documents, "document_id")
    route_ids = _unique_ids(routes, "task_id")
    _unique_ids(policies, "example_id")
    _unique_ids(policies, "source_task_id")

    route_by_id = {route["task_id"]: route for route in routes}
    family_counts: Counter[str] = Counter()
    route_splits: dict[str, set[str]] = defaultdict(set)
    split_counts: Counter[str] = Counter()

    for route in routes:
        family = route["pair_id"]
        if not family or not isinstance(family, str):
            raise ValueError("route family is blank or invalid")
        support = route["supporting_document_ids"]
        if not support or not set(support).issubset(doc_ids):
            raise ValueError(f"missing or unknown supporting documents: {route['task_id']}")
        family_counts[family] += 1

    for example in policies:
        split = example["split"]
        if split not in {"train", "dev", "heldout"}:
            raise ValueError(f"invalid supervised split: {split}")
        split_counts[split] += 1
        task = route_by_id.get(example["source_task_id"])
        if task is None:
            # Phase 11 includes valid older hard questions outside the route set.
            continue
        if example["question"] != task["question"]:
            raise ValueError(f"source question mismatch: {task['task_id']}")
        route_splits[task["pair_id"]].add(split)

    if set(route_splits) != set(family_counts):
        raise ValueError("some routing evidence families lack SFT split mappings")
    if any(len(splits) != 1 for splits in route_splits.values()):
        raise ValueError("evidence family is split across supervised partitions")
    if PREVIOUS_RL_TRAIN_FAMILY not in family_counts:
        raise ValueError("previous RL training family is absent")
    if len(route_ids) != len(routes):
        raise ValueError("invalid routing task IDs")

    return CampaignInventory(
        file_hashes=(
            (str(docs_path), docs_sha),
            (str(routes_path), routes_sha),
            (str(policies_path), policies_sha),
        ),
        document_count=len(documents),
        route_count=len(routes),
        policy_example_count=len(policies),
        route_families=tuple(sorted(family_counts)),
        route_family_counts=tuple(sorted(family_counts.items())),
        policy_split_counts=tuple(sorted(split_counts.items())),
        route_sft_split_by_family=tuple(
            sorted((family, next(iter(splits))) for family, splits in route_splits.items())
        ),
        previously_inspected_families=tuple(
            sorted(set(family_counts) - {PREVIOUS_RL_TRAIN_FAMILY})
        ),
    )


def main() -> None:
    inventory = build_inventory()
    print("Phase 13 EXP-120 — Campaign Provenance and Protocol Inventory")
    print("No training, no model evaluation, no new gold annotations.")
    for path, digest in inventory.file_hashes:
        print(f"SHA256 {path} = {digest}")
    print(
        f"documents={inventory.document_count} routes={inventory.route_count} "
        f"phase11_examples={inventory.policy_example_count} "
        f"route_families={len(inventory.route_families)}"
    )
    print(f"route_family_counts={dict(inventory.route_family_counts)}")
    print(f"phase11_split_counts={dict(inventory.policy_split_counts)}")
    print(f"route_family_phase11_splits={dict(inventory.route_sft_split_by_family)}")
    print(f"phase12_rl_train_family={PREVIOUS_RL_TRAIN_FAMILY}")
    print(f"phase12_inspected_heldout_families={inventory.previously_inspected_families}")
    print("PASS: IDs, supporting-document references, source question joins and")
    print("evidence-family supervised split membership are internally consistent.")
    print("WARNING: previously inspected heldout families are not pristine for")
    print("future adaptive-policy tuning; source NEW independent families first.")
    print("LIMIT: inventory is not model accuracy, retriever performance or")
    print("evidence that a new heldout benchmark exists.")


if __name__ == "__main__":
    main()
