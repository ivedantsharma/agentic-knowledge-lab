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
    scored_chunks: list[tuple[int, int, int, str, float]],
) -> tuple[int, int, int, str, float] | None:
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
        key=lambda item: item[4],
    )


def merge_chunk_window(
    section_text: str,
    chunks: list[tuple[int, int, int, str, float]],
) -> str:
    start_word = min(
        chunk[1]
        for chunk in chunks
    )
    end_word = max(
        chunk[2]
        for chunk in chunks
    )

    words = section_text.split()

    return " ".join(
        words[start_word:end_word]
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

    evidence_hits = 0
    total_naive_words = 0
    total_window_words = 0
    total_section_words = 0

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

        retained_windows = []
        naive_words = 0
        section_words = 0

        print(task.task_id)
        print(f"question={task.question}")

        for (
            document_id,
            section_index,
            section_title,
            section_text,
            _section_score,
        ) in retained_sections:
            document = next(
                item
                for item in documents
                if item.document_id == document_id
            )

            section_words += len(
                section_text.split()
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
                    chunk.start_word,
                    chunk.end_word,
                    str(chunk.metadata["raw_chunk_text"]),
                    float(score),
                )
                for chunk, score in zip(
                    chunks,
                    scores,
                )
            ]

            scored_chunks.sort(
                key=lambda item: item[4],
                reverse=True,
            )

            top_chunk = scored_chunks[0]
            neighbor = choose_neighbor(
                top_chunk[0],
                scored_chunks,
            )

            selected = [top_chunk]

            if neighbor is not None:
                selected.append(neighbor)

            naive_words += sum(
                len(item[3].split())
                for item in selected
            )

            window = merge_chunk_window(
                section_text,
                selected,
            )

            retained_windows.append(
                (
                    document_id,
                    section_title,
                    window,
                )
            )

            print(
                f"  section={document_id}::{section_title}"
            )
            print(
                f"    merged_window={window!r}"
            )
            print(
                "    merged_window_words="
                f"{len(window.split())}"
            )

        evidence_retained = any(
            task.evidence_text.casefold()
            in window.casefold()
            for (
                _document_id,
                _section_title,
                window,
            ) in retained_windows
        )

        window_words = sum(
            len(window.split())
            for (
                _document_id,
                _section_title,
                window,
            ) in retained_windows
        )

        evidence_hits += int(
            evidence_retained
        )
        total_naive_words += naive_words
        total_window_words += window_words
        total_section_words += section_words

        print(
            f"  evidence_retained={evidence_retained}"
        )
        print(
            f"  naive_retained_words={naive_words}"
        )
        print(
            f"  deduplicated_window_words={window_words}"
        )
        print(
            f"  full_section_words={section_words}"
        )
        print()

    task_count = len(tasks)

    avg_naive = (
        total_naive_words / task_count
    )
    avg_windows = (
        total_window_words / task_count
    )
    avg_sections = (
        total_section_words / task_count
    )

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "EvidenceRetentionRate="
        f"{evidence_hits / task_count:.4f}"
    )
    print(
        "AvgNaiveRetainedRawWords="
        f"{avg_naive:.2f}"
    )
    print(
        "AvgDeduplicatedWindowWords="
        f"{avg_windows:.2f}"
    )
    print(
        "AvgRetainedSectionWords="
        f"{avg_sections:.2f}"
    )
    print(
        "ReductionVsNaive="
        f"{1.0 - (avg_windows / avg_naive):.4f}"
    )
    print(
        "ReductionVsSections="
        f"{1.0 - (avg_windows / avg_sections):.4f}"
    )


if __name__ == "__main__":
    main()
