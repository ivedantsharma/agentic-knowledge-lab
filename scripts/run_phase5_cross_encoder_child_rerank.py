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

    document_hits = 0
    dense_hits = 0
    cross_hits = 0

    for task in tasks:
        document_ranking = retriever.rank_documents(
            task.question
        )
        document_id, document_score = document_ranking[0]
        document_hit = document_id == task.source_document_id

        dense_ranking = retriever.rank_sections(
            task.question,
            document_id,
        )
        dense_index, dense_title, dense_score = dense_ranking[0]

        selected_document = next(
            document
            for document in documents
            if document.document_id == document_id
        )

        pairs = [
            (
                task.question,
                render_section(selected_document, section),
            )
            for section in selected_document.sections
        ]

        scores = cross_encoder.predict(pairs)

        cross_ranking = sorted(
            [
                (
                    index,
                    selected_document.sections[index].title,
                    float(score),
                )
                for index, score in enumerate(scores)
            ],
            key=lambda item: item[2],
            reverse=True,
        )

        cross_index, cross_title, cross_score = cross_ranking[0]

        dense_hit = (
            task.evidence_text.casefold()
            in selected_document.sections[dense_index].text.casefold()
        )
        cross_hit = (
            task.evidence_text.casefold()
            in selected_document.sections[cross_index].text.casefold()
        )

        document_hits += int(document_hit)
        dense_hits += int(dense_hit)
        cross_hits += int(cross_hit)

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  document={document_id} "
            f"score={document_score:.6f} "
            f"hit={document_hit}"
        )
        print(
            "  dense_child="
            f"{dense_title} "
            f"score={dense_score:.6f} "
            f"hit={dense_hit}"
        )
        print("  cross_encoder_ranking=")
        for _index, title, score in cross_ranking:
            print(f"    {title}: {score:.6f}")
        print(
            "  cross_child="
            f"{cross_title} "
            f"score={cross_score:.6f} "
            f"hit={cross_hit}"
        )
        print()

    task_count = len(tasks)

    print("Aggregate")
    print(f"tasks={task_count}")
    print(
        "DocumentHit@1="
        f"{document_hits / task_count:.4f}"
    )
    print(
        "DenseChildHit@1="
        f"{dense_hits / task_count:.4f}"
    )
    print(
        "CrossEncoderChildHit@1="
        f"{cross_hits / task_count:.4f}"
    )


if __name__ == "__main__":
    main()