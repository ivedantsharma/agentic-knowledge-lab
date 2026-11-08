import json
from pathlib import Path

from knowledge_engine.ingestion.structured_schema import (
    StructuredDocument,
)

DATA_PATH = Path(
    "data/processed/phase5_parent_stress_documents_v0.json"
)


def test_parent_stress_dataset_has_base_and_distractor_documents() -> None:
    payload = json.loads(
        DATA_PATH.read_text(encoding="utf-8")
    )

    documents = [
        StructuredDocument.model_validate(item)
        for item in payload
    ]

    document_ids = {
        document.document_id
        for document in documents
    }

    assert {
        "manual_alpha",
        "manual_beta",
        "manual_gamma",
    }.issubset(document_ids)

    assert {
        "distractor_atlas_keys",
        "distractor_borealis_backup",
        "distractor_cirrus_failures",
    }.issubset(document_ids)

    assert all(
        len(document.sections) == 4
        for document in documents
    )
