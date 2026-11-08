import json
import sys
from pathlib import Path

from sentence_transformers import CrossEncoder, SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.hierarchical_chunker import chunk_section
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
SECTION_BEAM = 2
CHUNK_SIZE_WORDS = 10
CHUNK_OVERLAP_WORDS = 3


def load_evidence_tasks() -> list[EvidenceTask]:
    payload = json.loads(
        TASK_PATH.read_text(encoding="utf-8")
    )
    return [
        EvidenceTask.model_validate(item)
        for item in payload
    ]


def choose_neighbor(
    top_chunk_index: int,
    scored_chunks: list[tuple[int, str, str, float]],
) -> tuple[int, str, str, float] | None:
    by_index = {
        item[0]: item
        for item in scored_chunks
    }

    adjacent = [
        by_index[index]
        for index in (
            top_chunk_index - 1,
            top_chunk_index + 1,
        )
        if index in by_index
    ]

    if not adjacent:
        return None

    return max(
        adjacent,
        key=lambda item: item[3],
    )


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

    evidence_retention_hits = 0
    direct_top1_hits = 0
    neighbor_recovery_hits = 0
    total_retained_chunks = 0
    total_retained_raw_words = 0

    for task in tasks:
        document_ranking = retriever.rank_documents(
            task.question
        )

        selected_parent_ids = [
            document_id
            for document_id, _score
            in document_ranking[:PARENT_BEAM]
        ]

        section_candidates = []

        for document_id in selected_parent_ids:
            document = next(
                item
                for item in documents
                if item.document_id == document_id
            )

            for section_index, section in enumerate(
                document.sections
            ):
                section_candidates.append(
                    (
                        document_id,
                        section_index,
                        section.title,
                        render_section(document, section),
                        section.text,
                    )
                )

        section_scores = cross_encoder.predict(
            [
                (task.question, retrieval_text)
                for (
                    _document_id,
                    _section_index,
                    _section_title,
                    retrieval_text,
                    _raw_text,
                ) in section_candidates
            ]
        )

        section_ranking = sorted(
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
                    _retrieval_text,
                    raw_text,
                ), score in zip(
                    section_candidates,
                    section_scores,
                )
            ],
            key=lambda item: item[4],
            reverse=True,
        )

        retained_sections = section_ranking[:SECTION_BEAM]

        retained_chunks = []
        direct_top1_evidence = False

        print(task.task_id)
        print(f"question={task.question}")

        for (
            document_id,
            section_index,
            section_title,
            _section_text,
            _section_score,
        ) in retained_sections:
            document = next(
                item
                for item in documents
                if item.document_id == document_id
            )

            chunks = chunk_section(
                document,
                section_index=section_index,
                chunk_size_words=CHUNK_SIZE_WORDS,
                overlap_words=CHUNK_OVERLAP_WORDS,
            )

            scores = cross_encoder.predict(
                [
                    (task.question, chunk.text)
                    for chunk in chunks
                ]
            )

            scored_chunks = [
                (
                    chunk.chunk_index,
                    chunk.chunk_id,
                    str(chunk.metadata["raw_chunk_text"]),
                    float(score),
                )
                for chunk, score in zip(
                    chunks,
                    scores,
                )
            ]

            scored_chunks.sort(
                key=lambda item: item[3],
                reverse=True,
            )

            top_chunk = scored_chunks[0]
            neighbor = choose_neighbor(
                top_chunk[0],
                scored_chunks,
            )

            local_retained = [top_chunk]
            if neighbor is not None:
                local_retained.append(neighbor)

            top_contains_evidence = (
                task.evidence_text.casefold()
                in top_chunk[2].casefold()
            )
            direct_top1_evidence = (
                direct_top1_evidence
                or top_contains_evidence
            )

            print(
                f"  section={document_id}::{section_title}"
            )
            print(
                "    top_local="
                f"{top_chunk[1]} "
                f"score={top_chunk[3]:.6f} "
                f"raw_text={top_chunk[2]!r}"
            )

            if neighbor is not None:
                print(
                    "    neighbor="
                    f"{neighbor[1]} "
                    f"score={neighbor[3]:.6f} "
                    f"raw_text={neighbor[2]!r}"
                )

            for item in local_retained:
                retained_chunks.append(
                    (
                        document_id,
                        section_title,
                        item,
                    )
                )

        evidence_retained = any(
            task.evidence_text.casefold()
            in item[2][2].casefold()
            for item in retained_chunks
        )

        neighbor_recovered = (
            evidence_retained
            and not direct_top1_evidence
        )

        evidence_retention_hits += int(
            evidence_retained
        )
        direct_top1_hits += int(
            direct_top1_evidence
        )
        neighbor_recovery_hits += int(
            neighbor_recovered
        )
        total_retained_chunks += len(
            retained_chunks
        )
        total_retained_raw_words += sum(
            len(item[2][2].split())
            for item in retained_chunks
        )

        print(
            f"  direct_top1_evidence={direct_top1_evidence}"
        )
        print(
            f"  neighbor_recovered={neighbor_recovered}"
        )
        print(
            f"  evidence_retained={evidence_retained}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "DirectLocalTop1EvidenceRate="
        f"{direct_top1_hits / task_count:.4f}"
    )
    print(
        "NeighborRecoveryRate="
        f"{neighbor_recovery_hits / task_count:.4f}"
    )
    print(
        "EvidenceRetentionRate="
        f"{evidence_retention_hits / task_count:.4f}"
    )
    print(
        "AvgRetainedChunksPerQuery="
        f"{total_retained_chunks / task_count:.2f}"
    )
    print(
        "AvgRetainedRawWordsPerQuery="
        f"{total_retained_raw_words / task_count:.2f}"
    )


if __name__ == "__main__":
    main()
