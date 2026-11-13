"""EXP-122 Gate B2: same-source four-question system-level comparison.

This deliberately does NOT claim a causal representation-only ablation:
BM25, dense+cross-encoder hierarchy, and graph-path semantic rankers
are different complete systems. Gold is read only by the evaluator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.graph.path_search import SemanticGraphPathRanker
from knowledge_engine.graph.qa import ClaimGraphQAEngine
from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.coarse_to_fine import (
    CoarseToFineHierarchicalRetriever,
    HierarchicalRetrievalConfig,
)
from knowledgebench.datasets.representation_bridge import (
    CommonRepresentationSubstrate,
    build_common_substrate,
)
from knowledgebench.evaluation.phase13_representation_comparison import (
    SystemEvidenceResult,
    evaluate_system_outputs,
    summarize_scores,
)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"
MAX_ATOMS = 3
GRAPH_SHA = "4e3b26bd9dfbc57f57eb501132279f50e96be87e7db96ba7838d552a2669718e"
TASK_SHA = "767c9b0b2a3ea42d3d08407e1d095062790f770917d1e2452632adc5c9f0db9e"


def run_paired_systems(
    substrate: CommonRepresentationSubstrate,
    *,
    embedding_model: object,
    cross_encoder: object,
) -> list[SystemEvidenceResult]:
    """Search with question-only inputs; evaluator gold must not enter this method."""
    flat = substrate.flat_corpus()
    flat_ids = [atom_id for atom_id, _ in flat]
    flat_texts = [text for _, text in flat]
    bm25 = BM25Retriever(document_ids=flat_ids, document_texts=flat_texts)

    hierarchy = CoarseToFineHierarchicalRetriever(
        documents=list(substrate.hierarchy),
        embedding_model_name=EMBEDDING_MODEL,
        cross_encoder_model_name=CROSS_ENCODER_MODEL,
        config=HierarchicalRetrievalConfig(
            parent_beam=len(substrate.hierarchy),
            section_beam=MAX_ATOMS,
            chunk_size_words=10000,
            chunk_overlap_words=0,
            chunk_radius=0,
        ),
        embedding_model=embedding_model,
        cross_encoder=cross_encoder,
    )
    graph = ClaimGraphQAEngine(
        graph=substrate.graph,
        path_ranker=SemanticGraphPathRanker(
            model_name=EMBEDDING_MODEL, model=embedding_model
        ),
        max_hops=MAX_ATOMS,
    )
    section_to_atom = {
        (doc.document_id, index): str(section.metadata["atom_id"])
        for doc in substrate.hierarchy
        for index, section in enumerate(doc.sections)
    }
    claim_atoms: dict[str, list[str]] = {}
    for atom in substrate.atoms:
        claim_atoms.setdefault(atom.claim_id, []).append(atom.atom_id)
    outputs = []
    for task in substrate.tasks:
        question = task.question

        ranked_flat = [doc_id for doc_id, _ in bm25.rank(question, top_k=MAX_ATOMS)]
        flat_words = sum(len(flat_texts[flat_ids.index(atom_id)].split()) for atom_id in ranked_flat)
        outputs.append(SystemEvidenceResult(
            task_id=task.task_id, system="flat_bm25",
            atom_ids=tuple(ranked_flat), words_returned=flat_words,
            candidates_scored=len(flat),
        ))

        hierarchy_result = hierarchy.search(question)
        hierarchy_atoms = []
        hierarchy_words = 0
        for window in hierarchy_result.windows:
            key = (window.document_id, window.section_index)
            atom_id = section_to_atom[key]
            # Chunk settings should include the ENTIRE single-evidence section.
            source_atom = next(atom for atom in substrate.atoms if atom.atom_id == atom_id)
            if window.text != source_atom.evidence_text:
                raise ValueError("hierarchy returned truncated source evidence")
            hierarchy_atoms.append(atom_id)
            hierarchy_words += len(f"Relation: {window.section_title}. {window.text}".split())
        if len(hierarchy_atoms) > MAX_ATOMS:
            raise ValueError("hierarchy evidence exceeds budget")
        metadata = hierarchy_result.metadata
        outputs.append(SystemEvidenceResult(
            task_id=task.task_id, system="hierarchy",
            atom_ids=tuple(hierarchy_atoms),
            words_returned=hierarchy_words,
            candidates_scored=(
                int(metadata["parent_candidates_scored"])
                + int(metadata["section_candidates_scored"])
                + int(metadata["chunk_candidates_scored"])
            ),
        ))

        graph_result = graph.answer(question)
        graph_atoms = []
        for claim_id in graph_result.claim_ids:
            graph_atoms.extend(claim_atoms[claim_id])
        if len(graph_atoms) > MAX_ATOMS:
            raise ValueError("graph evidence exceeds budget")
        graph_words = sum(
            len(f"Relation: {atom.relation}. {atom.evidence_text}".split())
            for atom in substrate.atoms
            if atom.atom_id in set(graph_atoms)
        )
        outputs.append(SystemEvidenceResult(
            task_id=task.task_id, system="graph",
            atom_ids=tuple(graph_atoms),
            words_returned=graph_words,
            candidates_scored=graph_result.candidate_path_count,
            answer=graph_result.answer,
            claim_ids=tuple(graph_result.claim_ids),
        ))
    return outputs


def main() -> None:
    substrate = build_common_substrate()
    if substrate.source_sha256 != GRAPH_SHA or substrate.tasks_sha256 != TASK_SHA:
        raise ValueError("source hashes drifted from preregistered Gate B2")
    from sentence_transformers import CrossEncoder, SentenceTransformer

    embedder = SentenceTransformer(EMBEDDING_MODEL)
    reranker = CrossEncoder(CROSS_ENCODER_MODEL)
    outputs = run_paired_systems(
        substrate, embedding_model=embedder, cross_encoder=reranker
    )
    scores = evaluate_system_outputs(substrate, outputs, budget=MAX_ATOMS)
    summary = summarize_scores(scores)

    print("Phase 13 EXP-122 Gate B2 — Paired Representation SYSTEM Comparison")
    print("Same existing four graph-derived questions; 15 unchanged source evidence atoms.")
    print(f"models={EMBEDDING_MODEL} | {CROSS_ENCODER_MODEL}")
    print(f"budget=max_{MAX_ATOMS}_evidence_atoms per question")
    print("CAUTION: retrieval/ranking models differ; NOT causal representation-only ablation.")
    print("CAUTION: development tasks written for graph; NOT external generalization.")
    for task in substrate.tasks:
        print(f"{task.task_id} gold_claim_count={len(task.expected_claim_ids)}")
        for item in scores:
            if item.task_id == task.task_id:
                print(
                    f"  {item.system}: coverage={item.coverage:.4f} "
                    f"complete={item.complete} atoms={item.evidence_count} "
                    f"words={item.words_returned} candidates_scored={item.candidates_scored}"
                    + (
                        f" answer_correct={item.answer_correct} "
                        f"path_correct={item.claim_path_correct}"
                        if item.system == "graph" else ""
                    )
                )
    print("Aggregate")
    for system, metrics in summary.items():
        print(f"  {system} " + " ".join(f"{key}={value:.4f}" for key, value in metrics.items()))
    graph_scores = [x for x in scores if x.system == "graph"]
    print(
        "  graph_native_answer_exact_match="
        f"{sum(x.answer_correct is True for x in graph_scores) / len(graph_scores):.4f}"
        " (NOT comparable cross-system answer accuracy)"
    )
    print("Interpretation: evidence coverage and output context cost only comparable")
    print("at the capped output atom level; candidate scoring and architecture differ.")
    print("No final-answer generation for flat/hierarchy, no timed latency benchmark.")


if __name__ == "__main__":
    main()
