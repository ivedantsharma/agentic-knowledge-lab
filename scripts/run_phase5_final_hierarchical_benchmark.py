import json
import sys
from pathlib import Path

from sentence_transformers import CrossEncoder, SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)
from knowledge_engine.retrieval.coarse_to_fine import (
    CoarseToFineHierarchicalRetriever,
    HierarchicalRetrievalConfig,
)
from knowledgebench.tasks.evidence_schema import EvidenceTask

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

DOCUMENT_PATH = Path(
    "data/processed/phase5_long_section_documents_v0.json"
)
TASK_PATH = Path(
    "data/processed/phase5_long_section_tasks_v0.json"
)


def load_tasks() -> list[EvidenceTask]:
    payload = json.loads(
        TASK_PATH.read_text(encoding="utf-8")
    )
    return [
        EvidenceTask.model_validate(item)
        for item in payload
    ]


def main() -> None:
    documents = load_structured_documents_json(
        DOCUMENT_PATH
    )
    tasks = load_tasks()

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )
    cross_encoder = CrossEncoder(
        CROSS_ENCODER_MODEL
    )

    retriever = CoarseToFineHierarchicalRetriever(
        documents=documents,
        embedding_model_name=EMBEDDING_MODEL,
        cross_encoder_model_name=CROSS_ENCODER_MODEL,
        config=HierarchicalRetrievalConfig(
            parent_beam=2,
            section_beam=2,
            chunk_size_words=10,
            chunk_overlap_words=3,
            chunk_radius=1,
        ),
        embedding_model=embedding_model,
        cross_encoder=cross_encoder,
    )

    evidence_hits = 0
    total_window_words = 0

    for task in tasks:
        result = retriever.search(
            task.question
        )

        evidence_retained = any(
            task.evidence_text.casefold()
            in window.text.casefold()
            for window in result.windows
        )

        evidence_hits += int(
            evidence_retained
        )
        total_window_words += sum(
            len(window.text.split())
            for window in result.windows
        )

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  selected_parents={result.selected_parent_ids}"
        )
        for window in result.windows:
            print(
                "  window="
                f"{window.document_id}::{window.section_title} "
                f"section_score={window.section_score:.6f} "
                f"anchor_chunk={window.anchor_chunk_index} "
                f"anchor_score={window.anchor_chunk_score:.6f} "
                f"text={window.text!r}"
            )
        print(
            f"  evidence_retained={evidence_retained}"
        )
        print(
            f"  metadata={result.metadata}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "EvidenceRetentionRate="
        f"{evidence_hits / task_count:.4f}"
    )
    print(
        "AvgReturnedWindowWords="
        f"{total_window_words / task_count:.2f}"
    )


if __name__ == "__main__":
    main()
