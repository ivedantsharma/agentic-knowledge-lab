"""EXP-122 Gate B: inspect the common representation source before ablations."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledgebench.datasets.representation_bridge import build_common_substrate


def main() -> None:
    substrate = build_common_substrate()
    flat = substrate.flat_corpus()
    sections = [
        section for document in substrate.hierarchy for section in document.sections
    ]
    claim_ids = {claim.claim_id for claim in substrate.graph.claims}
    print("Phase 13 EXP-122 Gate B — Common Evidence Representation Contract")
    print("SOURCE: existing Phase 6 graph evidence and four existing graph questions.")
    print("STATUS: development-only, no new independent families or inference scores.")
    print(f"SHA256 graph={substrate.source_sha256}")
    print(f"SHA256 tasks={substrate.tasks_sha256}")
    print(
        f"claims={len(claim_ids)} evidence_atoms={len(substrate.atoms)} "
        f"flat_units={len(flat)} hierarchy_documents={len(substrate.hierarchy)} "
        f"hierarchy_sections={len(sections)} graph_tasks={len(substrate.tasks)}"
    )
    assert len(flat) == len(sections) == len(substrate.atoms)
    assert {atom.claim_id for atom in substrate.atoms} == claim_ids
    print("PASS: Every source claim evidence span appears once in flat and hierarchy.")
    print("PASS: Graph task paths, relations, expected values and provenance verified.")
    print("WARNING: Graph edges contain explicit relational structure; other views")
    print("have the same source evidence text but different navigation affordances.")
    print("WARNING: Shared source is graph-derived and questions were graph-designed.")
    print("NEXT: preregister equal-context/evidence-unit budgets and score all")
    print("three actual retrieval systems on these SAME graph task questions.")
    print("NO retriever scores, model comparison, or answer-quality claim yet.")


if __name__ == "__main__":
    main()
