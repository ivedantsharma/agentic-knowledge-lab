"""EXP-122 Gate A: source/schema comparability before representation ablations.

This is not a flat-vs-hierarchical-vs-graph performance benchmark.
It inventories distinct Phase 5 and Phase 6 source substrates and checks
whether any exact task mapping is already available.
"""

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

HIERARCHY_DOCS = Path("data/processed/phase5_long_section_documents_v0.json")
HIERARCHY_TASKS = Path("data/processed/phase5_long_section_tasks_v0.json")
GRAPH_SOURCE = Path("data/processed/phase6_branching_claim_graph_v0.json")
GRAPH_TASKS = Path("data/processed/phase6_graph_tasks_v0.json")


@dataclass(frozen=True)
class RepresentationSubstrateAudit:
    hashes: tuple[tuple[str, str], ...]
    hierarchy_documents: int
    hierarchy_sections: int
    hierarchy_tasks: int
    graph_entities: int
    graph_claims: int
    graph_tasks: int
    shared_task_ids: tuple[str, ...]
    shared_exact_questions: tuple[str, ...]
    shared_expected_answers: tuple[str, ...]
    complete_paired_task_crosswalk: bool


def _read(path: Path) -> tuple[object, str]:
    payload = path.read_bytes()
    return json.loads(payload), hashlib.sha256(payload).hexdigest()


def _unique(rows: list[dict], key: str) -> set[str]:
    values = [row[key] for row in rows]
    if any(not isinstance(v, str) or not v.strip() for v in values):
        raise ValueError(f"invalid {key}")
    if len(set(values)) != len(values):
        raise ValueError(f"duplicate {key}")
    return set(values)


def audit_substrates(
    hierarchy_docs_path: Path = HIERARCHY_DOCS,
    hierarchy_tasks_path: Path = HIERARCHY_TASKS,
    graph_path: Path = GRAPH_SOURCE,
    graph_tasks_path: Path = GRAPH_TASKS,
) -> RepresentationSubstrateAudit:
    docs, d_hash = _read(hierarchy_docs_path)
    tasks, t_hash = _read(hierarchy_tasks_path)
    graph, g_hash = _read(graph_path)
    graph_tasks, gt_hash = _read(graph_tasks_path)
    if not isinstance(docs, list) or not isinstance(tasks, list):
        raise TypeError("hierarchy sources must be lists")
    if not isinstance(graph, dict) or not isinstance(graph_tasks, list):
        raise TypeError("graph and graph tasks have unexpected shapes")
    if not docs or not tasks or not graph_tasks:
        raise ValueError("empty substrate cannot be compared")
    doc_ids = _unique(docs, "document_id")
    hierarchy_task_ids = _unique(tasks, "task_id")
    graph_task_ids = _unique(graph_tasks, "task_id")
    entity_ids = _unique(graph["entities"], "entity_id")
    claim_ids = _unique(graph["claims"], "claim_id")
    if not entity_ids or not claim_ids:
        raise ValueError("graph must contain entities and claims")
    sections = sum(len(doc["sections"]) for doc in docs)
    if any(not doc["sections"] for doc in docs):
        raise ValueError("hierarchy document has no sections")
    for task in tasks:
        if task["source_document_id"] not in doc_ids:
            raise ValueError("hierarchy evidence source is missing")
    for task in graph_tasks:
        if task["start_entity_id"] not in entity_ids:
            raise ValueError("graph start entity is missing")
        if not set(task["expected_claim_ids"]).issubset(claim_ids):
            raise ValueError("graph expected claim is missing")
    h_questions = {row["question"] for row in tasks}
    g_questions = {row["question"] for row in graph_tasks}
    h_answers = {row["expected_answer"] for row in tasks}
    g_answers = {row["expected_answer"] for row in graph_tasks}
    # An exact task ID+question/answer alignment would be a *necessary*
    # but not sufficient condition for a fair paired experiment.
    h_by_id = {row["task_id"]: row for row in tasks}
    g_by_id = {row["task_id"]: row for row in graph_tasks}
    shared = set(hierarchy_task_ids) & set(graph_task_ids)
    complete_crosswalk = (
        len(tasks) == len(graph_tasks)
        and shared == hierarchy_task_ids == graph_task_ids
        and all(
            h_by_id[key]["question"] == g_by_id[key]["question"]
            and h_by_id[key]["expected_answer"] == g_by_id[key]["expected_answer"]
            for key in shared
        )
    )
    return RepresentationSubstrateAudit(
        hashes=(
            (str(hierarchy_docs_path), d_hash),
            (str(hierarchy_tasks_path), t_hash),
            (str(graph_path), g_hash),
            (str(graph_tasks_path), gt_hash),
        ),
        hierarchy_documents=len(docs),
        hierarchy_sections=sections,
        hierarchy_tasks=len(tasks),
        graph_entities=len(entity_ids),
        graph_claims=len(claim_ids),
        graph_tasks=len(graph_tasks),
        shared_task_ids=tuple(sorted(shared)),
        shared_exact_questions=tuple(sorted(h_questions & g_questions)),
        shared_expected_answers=tuple(sorted(h_answers & g_answers)),
        complete_paired_task_crosswalk=complete_crosswalk,
    )


def main() -> None:
    result = audit_substrates()
    print("Phase 13 EXP-122 Gate A — Representation Substrate Compatibility")
    print("Provenance and task comparability only; NO architecture scores computed.")
    for path, digest in result.hashes:
        print(f"SHA256 {path} = {digest}")
    print(
        f"hierarchy_documents={result.hierarchy_documents} "
        f"hierarchy_sections={result.hierarchy_sections} "
        f"hierarchy_tasks={result.hierarchy_tasks}"
    )
    print(
        f"graph_entities={result.graph_entities} graph_claims={result.graph_claims} "
        f"graph_tasks={result.graph_tasks}"
    )
    print(f"shared_task_ids={result.shared_task_ids}")
    print(f"shared_exact_questions={result.shared_exact_questions}")
    print(f"shared_expected_answers={result.shared_expected_answers}")
    print(f"complete_paired_task_crosswalk={result.complete_paired_task_crosswalk}")
    if result.complete_paired_task_crosswalk:
        print("NECESSARY ID/question/answer alignment present; still audit source")
        print("information and evaluation-budget parity before running Gate B.")
    else:
        print("BLOCKED: no complete paired task crosswalk for fair architecture")
        print("comparison; historical Phase 5 and Phase 6 scores are incomparable.")
    print("Next: build and freeze a genuinely common source/evidence task mapping")
    print("before measuring flat vs hierarchy vs graph performance.")


if __name__ == "__main__":
    main()
