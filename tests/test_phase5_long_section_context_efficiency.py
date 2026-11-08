import json
from pathlib import Path

from knowledge_engine.ingestion.structured_schema import StructuredDocument

DATA_PATH = Path(
    "data/processed/phase5_long_section_documents_v0.json"
)


def test_long_section_stress_corpus_has_long_relevant_sections() -> None:
    payload = json.loads(
        DATA_PATH.read_text(encoding="utf-8")
    )

    documents = [
        StructuredDocument.model_validate(item)
        for item in payload
    ]

    relevant_ids = {
        "manual_alpha_long",
        "manual_beta_long",
        "manual_gamma_long",
    }

    relevant_documents = [
        document
        for document in documents
        if document.document_id in relevant_ids
    ]

    assert len(relevant_documents) == 3
    assert all(
        max(
            len(section.text.split())
            for section in document.sections
        ) >= 40
        for document in relevant_documents
    )
