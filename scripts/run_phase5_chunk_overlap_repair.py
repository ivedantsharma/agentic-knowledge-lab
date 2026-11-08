import json
import sys
from pathlib import Path

from sentence_transformers import CrossEncoder, SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.hierarchical_chunker import (
    chunk_section,
)
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
CHUNK_BEAM = 2


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

    fragmentation_count = 0
    chunk_top1_hits = 0
    chunk_top2_hits = 0
    chunk_retention_hits = 0
    total_chunks_scored = 0
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
                (task.question, candidate_text)
                for (
                    _document_id,
                    _section_index,
                    _section_title,
                    candidate_text,
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
                    _candidate_text,
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

        chunk_candidates = []

        for (
            document_id,
            section_index,
            section_title,
            _section_text,
            _score,
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

            for chunk in chunks:
                raw_chunk_text = str(
                    chunk.metadata["raw_chunk_text"]
                )
                chunk_candidates.append(
                    (
                        document_id,
                        section_title,
                        chunk.chunk_id,
                        chunk.text,
                        raw_chunk_text,
                    )
                )

        has_evidence_chunk = any(
            task.evidence_text.casefold()
            in item[4].casefold()
            for item in chunk_candidates
        )

        if not has_evidence_chunk:
            fragmentation_count += 1

        chunk_scores = cross_encoder.predict(
            [
                (task.question, retrieval_text)
                for (
                    _document_id,
                    _section_title,
                    _chunk_id,
                    retrieval_text,
                    _raw_text,
                ) in chunk_candidates
            ]
        )

        chunk_ranking = sorted(
            [
                (
                    document_id,
                    section_title,
                    chunk_id,
                    retrieval_text,
                    raw_text,
                    float(score),
                )
                for (
                    document_id,
                    section_title,
                    chunk_id,
                    retrieval_text,
                    raw_text,
                ), score in zip(
                    chunk_candidates,
                    chunk_scores,
                )
            ],
            key=lambda item: item[5],
            reverse=True,
        )

        relevant_rank = next(
            (
                index + 1
                for index, item in enumerate(chunk_ranking)
                if task.evidence_text.casefold()
                in item[4].casefold()
            ),
            None,
        )

        retained_chunks = chunk_ranking[:CHUNK_BEAM]

        evidence_retained = any(
            task.evidence_text.casefold()
            in item[4].casefold()
            for item in retained_chunks
        )

        chunk_top1_hits += int(relevant_rank == 1)
        chunk_top2_hits += int(
            relevant_rank is not None
            and relevant_rank <= 2
        )
        chunk_retention_hits += int(evidence_retained)
        total_chunks_scored += len(chunk_candidates)
        total_retained_raw_words += sum(
            len(item[4].split())
            for item in retained_chunks
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  evidence_chunk_exists={has_evidence_chunk}"
        )
        print(f"  relevant_chunk_rank={relevant_rank}")
        print("  retained_chunks=")
        for rank, item in enumerate(
            retained_chunks,
            start=1,
        ):
            print(
                f"    rank={rank} "
                f"{item[0]}::{item[1]}::{item[2]} "
                f"score={item[5]:.6f} "
                f"raw_text={item[4]!r}"
            )
        print(
            f"  evidence_retained={evidence_retained}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        f"EvidenceFragmentationCount={fragmentation_count}"
    )
    print(
        f"ChunkRecall@1={chunk_top1_hits / task_count:.4f}"
    )
    print(
        f"ChunkRecall@2={chunk_top2_hits / task_count:.4f}"
    )
    print(
        "ChunkEvidenceRetentionRate="
        f"{chunk_retention_hits / task_count:.4f}"
    )
    print(
        "AvgChunksScored="
        f"{total_chunks_scored / task_count:.2f}"
    )
    print(
        "AvgRetainedRawChunkWords="
        f"{total_retained_raw_words / task_count:.2f}"
    )


if __name__ == "__main__":
    main()
