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
CHUNK_OVERLAP_WORDS = 0
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

    parent_hits = 0
    section_retention_hits = 0
    chunk_top1_hits = 0
    chunk_top2_hits = 0
    chunk_retention_hits = 0
    total_section_words = 0
    total_retained_chunk_words = 0
    total_chunks_scored = 0

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
                        render_section(
                            document,
                            section,
                        ),
                        section.text,
                    )
                )

        section_pairs = [
            (task.question, candidate_text)
            for (
                _document_id,
                _section_index,
                _section_title,
                candidate_text,
                _raw_text,
            ) in section_candidates
        ]

        section_scores = cross_encoder.predict(
            section_pairs
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

        retained_sections = section_ranking[
            :SECTION_BEAM
        ]

        section_evidence_retained = any(
            task.evidence_text.casefold()
            in item[3].casefold()
            for item in retained_sections
        )

        section_words = sum(
            len(item[3].split())
            for item in retained_sections
        )

        chunk_candidates = []

        for (
            document_id,
            section_index,
            section_title,
            _raw_text,
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
                chunk_candidates.append(
                    (
                        document_id,
                        section_index,
                        section_title,
                        chunk.chunk_id,
                        chunk.text,
                    )
                )

        chunk_pairs = [
            (task.question, chunk_text)
            for (
                _document_id,
                _section_index,
                _section_title,
                _chunk_id,
                chunk_text,
            ) in chunk_candidates
        ]

        chunk_scores = cross_encoder.predict(
            chunk_pairs
        )

        chunk_ranking = sorted(
            [
                (
                    document_id,
                    section_index,
                    section_title,
                    chunk_id,
                    chunk_text,
                    float(score),
                )
                for (
                    document_id,
                    section_index,
                    section_title,
                    chunk_id,
                    chunk_text,
                ), score in zip(
                    chunk_candidates,
                    chunk_scores,
                )
            ],
            key=lambda item: item[5],
            reverse=True,
        )

        relevant_chunk_rank = next(
            (
                index + 1
                for index, item in enumerate(
                    chunk_ranking
                )
                if task.evidence_text.casefold()
                in item[4].casefold()
            ),
            None,
        )

        retained_chunks = chunk_ranking[:CHUNK_BEAM]

        chunk_evidence_retained = any(
            task.evidence_text.casefold()
            in item[4].casefold()
            for item in retained_chunks
        )

        retained_chunk_words = sum(
            len(item[4].split())
            for item in retained_chunks
        )

        parent_hits += int(parent_hit)
        section_retention_hits += int(
            section_evidence_retained
        )
        chunk_top1_hits += int(
            relevant_chunk_rank == 1
        )
        chunk_top2_hits += int(
            relevant_chunk_rank is not None
            and relevant_chunk_rank <= 2
        )
        chunk_retention_hits += int(
            chunk_evidence_retained
        )
        total_section_words += section_words
        total_retained_chunk_words += (
            retained_chunk_words
        )
        total_chunks_scored += len(
            chunk_candidates
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  selected_parents={selected_parent_ids}"
        )
        print(f"  parent_hit={parent_hit}")
        print("  retained_sections=")
        for rank, item in enumerate(
            retained_sections,
            start=1,
        ):
            print(
                f"    rank={rank} "
                f"{item[0]}::{item[2]} "
                f"score={item[4]:.6f}"
            )
        print(
            "  section_evidence_retained="
            f"{section_evidence_retained}"
        )
        print(
            f"  section_context_words={section_words}"
        )
        print(
            f"  relevant_chunk_rank={relevant_chunk_rank}"
        )
        print("  retained_chunks=")
        for rank, item in enumerate(
            retained_chunks,
            start=1,
        ):
            print(
                f"    rank={rank} "
                f"{item[0]}::{item[2]}::{item[3]} "
                f"score={item[5]:.6f} "
                f"text={item[4]!r}"
            )
        print(
            "  chunk_evidence_retained="
            f"{chunk_evidence_retained}"
        )
        print(
            "  retained_chunk_words="
            f"{retained_chunk_words}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        f"ParentRecall@2={parent_hits / task_count:.4f}"
    )
    print(
        "SectionEvidenceRetentionRate="
        f"{section_retention_hits / task_count:.4f}"
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
        "AvgSectionContextWords="
        f"{total_section_words / task_count:.2f}"
    )
    print(
        "AvgRetainedChunkWords="
        f"{total_retained_chunk_words / task_count:.2f}"
    )
    print(
        "AvgChunksScored="
        f"{total_chunks_scored / task_count:.2f}"
    )


if __name__ == "__main__":
    main()
