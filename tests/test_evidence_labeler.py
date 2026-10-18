from knowledge_engine.ingestion.chunker import chunk_by_words
from knowledge_engine.ingestion.schema import SourceDocument
from knowledgebench.tasks.evidence_labeler import derive_chunk_task
from knowledgebench.tasks.evidence_schema import EvidenceTask


def test_derive_chunk_task_finds_evidence_chunk() -> None:
    document = SourceDocument(
        document_id="doc",
        text="alpha beta TARGET gamma delta",
    )

    chunks = chunk_by_words(
        document,
        chunk_size_words=3,
        overlap_words=1,
    )

    evidence_task = EvidenceTask(
        task_id="q1",
        question="Where is the target?",
        source_document_id="doc",
        evidence_text="TARGET",
    )

    task = derive_chunk_task(evidence_task, chunks)

    assert task.relevant_document_ids


def test_derive_chunk_task_can_return_multiple_relevant_chunks() -> None:
    document = SourceDocument(
        document_id="doc",
        text="a b c TARGET d e f",
    )

    chunks = chunk_by_words(
        document,
        chunk_size_words=5,
        overlap_words=3,
    )

    evidence_task = EvidenceTask(
        task_id="q1",
        question="Find target",
        source_document_id="doc",
        evidence_text="TARGET",
    )

    task = derive_chunk_task(evidence_task, chunks)

    assert len(task.relevant_document_ids) >= 2


def test_derive_chunk_task_does_not_match_other_source_document() -> None:
    documents = [
        SourceDocument(document_id="a", text="TARGET here"),
        SourceDocument(document_id="b", text="TARGET here too"),
    ]

    chunks = [
        chunk
        for document in documents
        for chunk in chunk_by_words(document, chunk_size_words=5)
    ]

    evidence_task = EvidenceTask(
        task_id="q1",
        question="Find target",
        source_document_id="a",
        evidence_text="TARGET",
    )

    task = derive_chunk_task(evidence_task, chunks)

    assert all(
        chunk_id.startswith("a::")
        for chunk_id in task.relevant_document_ids
    )
