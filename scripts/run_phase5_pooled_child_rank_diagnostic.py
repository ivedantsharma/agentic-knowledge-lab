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
CHILD_KS = (1, 2, 3)


def load_evidence_tasks() -> list[EvidenceTask]:
    payload = json.loads(
        TASK_PATH.read_text(encoding="utf-8")
    )
    return [
        EvidenceTask.model_validate(item)
        for item in payload
    ]


def reciprocal_rank(rank: int | None) -> float:
    if rank is None:
        return 0.0
    return 1.0 / rank


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

    recall_hits = {
        beam: {k: 0 for k in CHILD_KS}
        for beam in PARENT_BEAMS
    }
    reciprocal_ranks = {
        beam: 0.0
        for beam in PARENT_BEAMS
    }

    for task in tasks:
        document_ranking = retriever.rank_documents(
            task.question
        )

        print(task.task_id)
        print(f"question={task.question}")

        for beam in PARENT_BEAMS:
            selected_parent_ids = [
                document_id
                for document_id, _score
                in document_ranking[:beam]
            ]

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

            relevant_rank = next(
                (
                    index + 1
                    for index, item in enumerate(ranking)
                    if task.evidence_text.casefold()
                    in item[3].casefold()
                ),
                None,
            )

            reciprocal_ranks[beam] += reciprocal_rank(
                relevant_rank
            )

            for k in CHILD_KS:
                if (
                    relevant_rank is not None
                    and relevant_rank <= k
                ):
                    recall_hits[beam][k] += 1

            print(
                f"  beam={beam} "
                f"relevant_child_rank={relevant_rank}"
            )
            for rank, item in enumerate(
                ranking[:5],
                start=1,
            ):
                print(
                    f"    rank={rank} "
                    f"{item[0]}::{item[2]} "
                    f"score={item[4]:.6f}"
                )

        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")

    for beam in PARENT_BEAMS:
        for k in CHILD_KS:
            print(
                f"ChildRecall@{k}_beam{beam}="
                f"{recall_hits[beam][k] / task_count:.4f}"
            )

        print(
            f"ChildMRR_beam{beam}="
            f"{reciprocal_ranks[beam] / task_count:.4f}"
        )


if __name__ == "__main__":
    main()
