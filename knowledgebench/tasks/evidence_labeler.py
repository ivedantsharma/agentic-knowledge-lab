from knowledge_engine.ingestion.schema import DocumentChunk
from knowledgebench.tasks.evidence_schema import EvidenceTask
from knowledgebench.tasks.schema import KnowledgeTask


def derive_chunk_task(
    evidence_task: EvidenceTask,
    chunks: list[DocumentChunk],
) -> KnowledgeTask:
    """Convert source-level evidence into chunk-level relevance labels."""
    evidence = evidence_task.evidence_text.casefold()

    relevant_chunk_ids = {
        chunk.chunk_id
        for chunk in chunks
        if chunk.source_document_id == evidence_task.source_document_id
        and evidence in chunk.text.casefold()
    }

    return KnowledgeTask(
        task_id=evidence_task.task_id,
        question=evidence_task.question,
        relevant_document_ids=relevant_chunk_ids,
        category=evidence_task.category,
        expected_answer=evidence_task.expected_answer,
        metadata={
            **evidence_task.metadata,
            "source_document_id": evidence_task.source_document_id,
            "evidence_text": evidence_task.evidence_text,
        },
    )
