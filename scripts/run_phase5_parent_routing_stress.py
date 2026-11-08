import json
import sys
from pathlib import Path

from sentence_transformers import CrossEncoder, SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)
from knowledge_engine.retrieval.hierarchical import (
    HierarchicalDenseRetriever,
    render_section,
)
from knowledgebench.tasks.evidence_schema import EvidenceTask


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

STRUCTURED_PATH = Path(
    "data/processed/phase5_parent_stress_documents_v0.json"
)
TASK_PATH = Path(
    "data/processed/phase2_evidence_tasks_v0.json"
)

PARENT_BEAMS = (1, 2, 3)


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

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )
    cross_encoder = CrossEncoder(
        CROSS_ENCODER_MODEL
    )

    retriever = HierarchicalDenseRetriever(
        documents=documents,
        model_name=EMBEDDING_MODEL,
        model=embedding_model,
    )

    parent_recall_hits = {
        beam: 0
        for beam in PARENT_BEAMS
    }
    end_to_end_hits = {
        beam: 0
        for beam in PARENT_BEAMS
    }
    child_candidates = {
        beam: 0
        for beam in PARENT_BEAMS
    }

    for task in tasks:
        document_ranking = retriever.rank_documents(
            task.question
        )

        parent_rank = next(
            index + 1
            for index, (document_id, _score)
            in enumerate(document_ranking)
            if document_id == task.source_document_id
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(f"  correct_parent_rank={parent_rank}")
        print("  document_ranking=")

        for document_id, score in document_ranking:
            print(
                f"    {document_id}: {score:.6f}"
            )

        for beam in PARENT_BEAMS:
            selected_parent_ids = [
                document_id
                for document_id, _score
                in document_ranking[:beam]
            ]

            parent_recall = (
                task.source_document_id
                in selected_parent_ids
            )

            candidate_sections = []

            for document_id in selected_parent_ids:
                document = next(
                    item
                    for item in documents
                    if item.document_id == document_id
                )

                for section_index, section in enumerate(
                    document.sections
                ):
                    candidate_sections.append(
                        (
                            document_id,
                            section_index,
                            section.title,
                            render_section(
                                document,
                                section,
                            ),
                            section.text,
                        )
                    )

            pairs = [
                (
                    task.question,
                    candidate_text,
                )
                for (
                    _document_id,
                    _section_index,
                    _section_title,
                    candidate_text,
                    _raw_text,
                ) in candidate_sections
            ]

            scores = cross_encoder.predict(pairs)

            ranking = sorted(
                [
                    (
                        document_id,
                        section_index,
                        section_title,
                        raw_text,
                        float(score),
                    )
                    for (
                        document_id,
                        section_index,
                        section_title,
                        _candidate_text,
                        raw_text,
                    ), score in zip(
                        candidate_sections,
                        scores,
                    )
                ],
                key=lambda item: item[4],
                reverse=True,
            )

            top = ranking[0]

            hit = (
                task.evidence_text.casefold()
                in top[3].casefold()
            )

            parent_recall_hits[beam] += int(
                parent_recall
            )
            end_to_end_hits[beam] += int(hit)
            child_candidates[beam] += len(
                candidate_sections
            )

            print(
                f"  beam={beam} "
                f"parent_recall={parent_recall} "
                f"child_candidates={len(candidate_sections)}"
            )
            print(
                "    top_child="
                f"{top[0]}::{top[2]} "
                f"score={top[4]:.6f} "
                f"hit={hit}"
            )

        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")

    for beam in PARENT_BEAMS:
        print(
            f"ParentRecall@{beam}="
            f"{parent_recall_hits[beam] / task_count:.4f}"
        )
        print(
            f"EndToEndHit@1_beam{beam}="
            f"{end_to_end_hits[beam] / task_count:.4f}"
        )
        print(
            f"AvgChildCandidates_beam{beam}="
            f"{child_candidates[beam] / task_count:.2f}"
        )


if __name__ == "__main__":
    main()
