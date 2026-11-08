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

PARENT_BEAM = 2
CHILD_BEAM = 2


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

    parent_hits = 0
    child_top1_hits = 0
    child_top2_hits = 0
    retained_evidence_hits = 0

    for task in tasks:
        document_ranking = retriever.rank_documents(
            task.question
        )

        selected_parent_ids = [
            document_id
            for document_id, _score
            in document_ranking[:PARENT_BEAM]
        ]

        parent_hit = (
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
            (task.question, candidate_text)
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

        retained = ranking[:CHILD_BEAM]

        relevant_rank = next(
            (
                index + 1
                for index, item in enumerate(ranking)
                if task.evidence_text.casefold()
                in item[3].casefold()
            ),
            None,
        )

        top1_hit = relevant_rank == 1
        top2_hit = (
            relevant_rank is not None
            and relevant_rank <= 2
        )

        retained_evidence = any(
            task.evidence_text.casefold()
            in item[3].casefold()
            for item in retained
        )

        parent_hits += int(parent_hit)
        child_top1_hits += int(top1_hit)
        child_top2_hits += int(top2_hit)
        retained_evidence_hits += int(
            retained_evidence
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  selected_parents={selected_parent_ids}"
        )
        print(f"  parent_hit={parent_hit}")
        print(
            f"  relevant_child_rank={relevant_rank}"
        )
        print("  retained_children=")
        for rank, item in enumerate(
            retained,
            start=1,
        ):
            print(
                f"    rank={rank} "
                f"{item[0]}::{item[2]} "
                f"score={item[4]:.6f}"
            )
        print(
            f"  evidence_retained={retained_evidence}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        f"ParentRecall@2={parent_hits / task_count:.4f}"
    )
    print(
        f"ChildRecall@1={child_top1_hits / task_count:.4f}"
    )
    print(
        f"ChildRecall@2={child_top2_hits / task_count:.4f}"
    )
    print(
        "EvidenceRetentionRate="
        f"{retained_evidence_hits / task_count:.4f}"
    )
    print(
        f"RetainedChildrenPerQuery={float(CHILD_BEAM):.2f}"
    )
    print(
        "ScoredChildrenPerQuery="
        f"{float(PARENT_BEAM * 4):.2f}"
    )


if __name__ == "__main__":
    main()
