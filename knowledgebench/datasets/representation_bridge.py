"""EXP-122 Gate B: lossless evidence projection from ONE existing claim graph.

This constructs a common *development* substrate. It does not invent new
facts, fabricate heldout questions, run retrieval, or report accuracy.
The native graph supplies the only source facts; all variants use its
unchanged evidence text. Structured edges remain an architectural difference.
"""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from knowledge_engine.graph.schema import ClaimGraph
from knowledge_engine.ingestion.structured_schema import (
    DocumentSection,
    StructuredDocument,
)
from knowledgebench.tasks.graph_schema import GraphTraversalTask

DEFAULT_GRAPH = Path("data/processed/phase6_branching_claim_graph_v0.json")
DEFAULT_TASKS = Path("data/processed/phase6_graph_tasks_v0.json")


@dataclass(frozen=True)
class EvidenceAtom:
    atom_id: str
    claim_id: str
    document_id: str
    subject_entity_id: str
    relation: str
    evidence_text: str


@dataclass(frozen=True)
class CommonRepresentationSubstrate:
    source_sha256: str
    tasks_sha256: str
    graph: ClaimGraph
    tasks: tuple[GraphTraversalTask, ...]
    atoms: tuple[EvidenceAtom, ...]
    hierarchy: tuple[StructuredDocument, ...]

    def flat_corpus(self) -> tuple[tuple[str, str], ...]:
        """One unchanged evidence span per claim reference, with relation label.

        The relation is also available as the hierarchy section title.
        No gold task answer/expected path is added to this corpus.
        """
        return tuple(
            (atom.atom_id, f"Relation: {atom.relation}. {atom.evidence_text}")
            for atom in self.atoms
        )


def _validate_task_paths(
    graph: ClaimGraph,
    tasks: tuple[GraphTraversalTask, ...],
) -> None:
    claims = {claim.claim_id: claim for claim in graph.claims}
    seen: set[str] = set()
    for task in tasks:
        if task.task_id in seen:
            raise ValueError("duplicate graph task IDs")
        seen.add(task.task_id)
        if len(task.expected_claim_ids) != len(task.relation_path):
            raise ValueError(f"claim/relation path length mismatch: {task.task_id}")
        current = task.start_entity_id
        for claim_id, relation in zip(task.expected_claim_ids, task.relation_path):
            claim = claims.get(claim_id)
            if claim is None:
                raise ValueError(f"task refers to missing claim: {task.task_id}")
            if claim.subject_entity_id != current or claim.relation != relation:
                raise ValueError(f"task path continuity/relation mismatch: {task.task_id}")
            if claim.object_entity_id is not None:
                current = claim.object_entity_id
            elif claim_id != task.expected_claim_ids[-1]:
                raise ValueError(f"literal-valued nonterminal edge: {task.task_id}")
        terminal = claims[task.expected_claim_ids[-1]]
        if terminal.object_value != task.expected_answer:
            raise ValueError(f"task expected answer disagrees with graph: {task.task_id}")


def build_common_substrate(
    graph_path: Path = DEFAULT_GRAPH,
    tasks_path: Path = DEFAULT_TASKS,
) -> CommonRepresentationSubstrate:
    graph_bytes = graph_path.read_bytes()
    task_bytes = tasks_path.read_bytes()
    graph = ClaimGraph.model_validate_json(graph_bytes)
    # Parse the same source tasks without altering their question text.
    raw_tasks = json.loads(task_bytes)
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise ValueError("graph tasks must be a nonempty list")
    tasks = tuple(GraphTraversalTask.model_validate(item) for item in raw_tasks)
    _validate_task_paths(graph, tasks)

    atoms = tuple(
        EvidenceAtom(
            atom_id=f"{claim.claim_id}#{index}",
            claim_id=claim.claim_id,
            document_id=ref.document_id,
            subject_entity_id=claim.subject_entity_id,
            relation=claim.relation,
            evidence_text=ref.evidence_text,
        )
        for claim in graph.claims
        for index, ref in enumerate(claim.evidence)
    )
    if len(atoms) != len({atom.atom_id for atom in atoms}):
        raise ValueError("duplicate evidence atom IDs")

    # Preserve every original evidence span as a section. Entity grouping
    # is derived solely from claim provenance, not gold task paths.
    subject_ids = tuple(dict.fromkeys(atom.subject_entity_id for atom in atoms))
    hierarchy = tuple(
        StructuredDocument(
            document_id=subject_id,
            sections=[
                DocumentSection(
                    title=atom.relation,
                    text=atom.evidence_text,
                    metadata={
                        "atom_id": atom.atom_id,
                        "claim_id": atom.claim_id,
                        "source_document_id": atom.document_id,
                    },
                )
                for atom in atoms if atom.subject_entity_id == subject_id
            ],
            metadata={"source": "phase6_graph_claim_evidence", "entity_id": subject_id},
        )
        for subject_id in subject_ids
    )
    flat_ids = {atom.atom_id for atom in atoms}
    section_ids = {
        str(section.metadata["atom_id"])
        for document in hierarchy
        for section in document.sections
    }
    if flat_ids != section_ids or len(flat_ids) != sum(
        len(document.sections) for document in hierarchy
    ):
        raise ValueError("evidence atoms not preserved across representations")
    return CommonRepresentationSubstrate(
        source_sha256=hashlib.sha256(graph_bytes).hexdigest(),
        tasks_sha256=hashlib.sha256(task_bytes).hexdigest(),
        graph=graph,
        tasks=tasks,
        atoms=atoms,
        hierarchy=hierarchy,
    )
