import json
import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)
from knowledge_engine.retrieval.hierarchical import (
    HierarchicalDenseRetriever,
    render_section,
)
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledgebench.tasks.evidence_schema import EvidenceTask

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
STRUCTURED_PATH = Path(
    "data/processed/phase2_structured_documents_v0.json"
)
TASK_PATH = Path(
    "data/processed/phase2_evidence_tasks_v0.json"
)


def load_evidence_tasks() -> list[EvidenceTask]:
    payload = json.loads(
        TASK_PATH.read_text(encoding="utf-8")
    )
    return [
        EvidenceTask.model_validate(item)
        for item in payload
    ]


def main() -> None:
    documents = load_structured_documents_json(
        STRUCTURED_PATH
    )
    tasks = load_evidence_tasks()

    model = SentenceTransformer(MODEL_NAME)

    retriever = HierarchicalDenseRetriever(
        documents=documents,
        model_name=MODEL_NAME,
        model=model,
    )

    flat_sections: list[tuple[str, int, str, str]] = []

    for document in documents:
        for index, section in enumerate(document.sections):
            flat_sections.append(
                (
                    document.document_id,
                    index,
                    section.title,
                    render_section(document, section),
                )
            )

    flat_embeddings = model.encode(
        [item[3] for item in flat_sections]
    )

    document_hits = 0
    flat_section_hits = 0
    hierarchical_section_hits = 0
    total_hierarchical_child_candidates = 0

    for task in tasks:
        query_embedding = model.encode(
            task.question
        ).tolist()

        flat_ranking = [
            (
                document_id,
                section_index,
                section_title,
                cosine_similarity(
                    query_embedding,
                    embedding.tolist(),
                ),
            )
            for (
                document_id,
                section_index,
                section_title,
                _text,
            ), embedding in zip(
                flat_sections,
                flat_embeddings,
            )
        ]
        flat_ranking.sort(
            key=lambda item: item[3],
            reverse=True,
        )

        flat_top = flat_ranking[0]
        flat_document = next(
            document
            for document in documents
            if document.document_id == flat_top[0]
        )
        flat_section = flat_document.sections[
            flat_top[1]
        ]
        flat_hit = (
            task.evidence_text.casefold()
            in flat_section.text.casefold()
        )

        document_ranking = retriever.rank_documents(
            task.question
        )
        document_id, document_score = (
            document_ranking[0]
        )
        document_hit = (
            document_id == task.source_document_id
        )

        section_ranking = retriever.rank_sections(
            task.question,
            document_id,
        )
        total_hierarchical_child_candidates += len(
            section_ranking
        )
        section_index, section_title, section_score = (
            section_ranking[0]
        )
        selected_document = next(
            document
            for document in documents
            if document.document_id == document_id
        )
        selected_section = selected_document.sections[
            section_index
        ]
        hierarchical_hit = (
            task.evidence_text.casefold()
            in selected_section.text.casefold()
        )

        document_hits += int(document_hit)
        flat_section_hits += int(flat_hit)
        hierarchical_section_hits += int(
            hierarchical_hit
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(
            "  flat_top="
            f"{flat_top[0]}::{flat_top[2]} "
            f"score={flat_top[3]:.6f} "
            f"hit={flat_hit}"
        )
        print(
            "  document_top="
            f"{document_id} "
            f"score={document_score:.6f} "
            f"hit={document_hit}"
        )
        print(
            "  hierarchical_section_top="
            f"{document_id}::{section_title} "
            f"score={section_score:.6f} "
            f"hit={hierarchical_hit}"
        )
        print()

    task_count = len(tasks)
    flat_candidate_count = len(flat_sections)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "DocumentHit@1="
        f"{document_hits / task_count:.4f}"
    )
    print(
        "FlatSectionHit@1="
        f"{flat_section_hits / task_count:.4f}"
    )
    print(
        "HierarchicalSectionHit@1="
        f"{hierarchical_section_hits / task_count:.4f}"
    )
    print(
        "FlatCandidateCountPerQuery="
        f"{float(flat_candidate_count):.2f}"
    )
    print(
        "HierarchicalChildCandidatesPerQuery="
        f"{total_hierarchical_child_candidates / task_count:.2f}"
    )


if __name__ == "__main__":
    main()