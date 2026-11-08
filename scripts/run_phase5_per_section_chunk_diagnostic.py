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

        pooled_chunks = []

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

            pairs = [
                (task.question, chunk.text)
                for chunk in chunks
            ]
            scores = cross_encoder.predict(pairs)

            local_ranking = sorted(
                [
                    (
                        document_id,
                        section_title,
                        chunk.chunk_id,
                        str(chunk.metadata["raw_chunk_text"]),
                        float(score),
                    )
                    for chunk, score in zip(chunks, scores)
                ],
                key=lambda item: item[4],
                reverse=True,
            )

            relevant_local_rank = next(
                (
                    rank
                    for rank, item in enumerate(
                        local_ranking,
                        start=1,
                    )
                    if task.evidence_text.casefold()
                    in item[3].casefold()
                ),
                None,
            )

            print(
                f"  section={document_id}::{section_title} "
                f"relevant_local_rank={relevant_local_rank}"
            )

            for rank, item in enumerate(
                local_ranking,
                start=1,
            ):
                print(
                    f"    local_rank={rank} "
                    f"score={item[4]:.6f} "
                    f"raw_text={item[3]!r}"
                )

            pooled_chunks.extend(local_ranking)

        pooled_ranking = sorted(
            pooled_chunks,
            key=lambda item: item[4],
            reverse=True,
        )

        relevant_global_rank = next(
            (
                rank
                for rank, item in enumerate(
                    pooled_ranking,
                    start=1,
                )
                if task.evidence_text.casefold()
                in item[3].casefold()
            ),
            None,
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  relevant_global_rank={relevant_global_rank}"
        )
        print()


if __name__ == "__main__":
    main()
