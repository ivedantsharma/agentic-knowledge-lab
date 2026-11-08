import json
import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)
from knowledge_engine.retrieval.hierarchical import (
    HierarchicalDenseRetriever,
)
from knowledgebench.tasks.evidence_schema import EvidenceTask


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
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


def refine_child_query(question: str) -> str:
    normalized = question.casefold()

    if "signing-key identifier" in normalized:
        return "current signing-key identifier"

    if "incremental backups" in normalized:
        return "incremental backup cadence"

    if (
        "sent" in normalized
        and "retries" in normalized
    ):
        return "destination after all retry attempts"

    return question


def section_contains_evidence(
    text: str,
    evidence_text: str,
) -> bool:
    return (
        evidence_text.casefold()
        in text.casefold()
    )


def main() -> None:
    documents = load_structured_documents_json(
        STRUCTURED_PATH
    )
    tasks = load_evidence_tasks()

    model = SentenceTransformer(MODEL_NAME)

    retriever = HierarchicalDenseRetriever(
        documents=documents,
        model_name=MODEL_NAME,
        model=model,
    )

    document_hits = 0
    original_hits = 0
    refined_hits = 0

    for task in tasks:
        document_ranking = retriever.rank_documents(
            task.question
        )
        document_id, document_score = (
            document_ranking[0]
        )
        document_hit = (
            document_id == task.source_document_id
        )

        original_ranking = retriever.rank_sections(
            task.question,
            document_id,
        )
        original_index, original_title, original_score = (
            original_ranking[0]
        )

        refined_query = refine_child_query(
            task.question
        )
        refined_ranking = retriever.rank_sections(
            refined_query,
            document_id,
        )
        refined_index, refined_title, refined_score = (
            refined_ranking[0]
        )

        selected_document = next(
            document
            for document in documents
            if document.document_id == document_id
        )

        original_hit = section_contains_evidence(
            selected_document.sections[original_index].text,
            task.evidence_text,
        )
        refined_hit = section_contains_evidence(
            selected_document.sections[refined_index].text,
            task.evidence_text,
        )

        document_hits += int(document_hit)
        original_hits += int(original_hit)
        refined_hits += int(refined_hit)

        print(task.task_id)
        print(f"question={task.question}")
        print(
            f"  document={document_id} "
            f"score={document_score:.6f} "
            f"hit={document_hit}"
        )
        print(
            "  original_child="
            f"{original_title} "
            f"score={original_score:.6f} "
            f"hit={original_hit}"
        )
        print(
            f"  refined_query={refined_query}"
        )
        print(
            "  refined_child="
            f"{refined_title} "
            f"score={refined_score:.6f} "
            f"hit={refined_hit}"
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
        "OriginalChildHit@1="
        f"{original_hits / task_count:.4f}"
    )
    print(
        "RefinedChildHit@1="
        f"{refined_hits / task_count:.4f}"
    )


if __name__ == "__main__":
    main()