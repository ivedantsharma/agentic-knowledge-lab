import json

from knowledge_engine.ingestion.structured_loader import (
    load_structured_documents_json,
)


def test_load_structured_documents_json(tmp_path) -> None:
    path = tmp_path / "structured.json"

    path.write_text(
        json.dumps(
            [
                {
                    "document_id": "doc-1",
                    "sections": [
                        {
                            "title": "Intro",
                            "text": "Hello world",
                        }
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )

    documents = load_structured_documents_json(path)

    assert len(documents) == 1
    assert documents[0].document_id == "doc-1"
    assert documents[0].sections[0].title == "Intro"
