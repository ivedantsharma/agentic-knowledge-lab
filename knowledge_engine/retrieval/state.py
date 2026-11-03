from pydantic import BaseModel, Field


class RetrievalState(BaseModel):
    """State carried between retrieval hops."""

    entity: str | None = None
    qualifiers: list[str] = Field(default_factory=list)
    source_document_id: str | None = None
    evidence_text: str | None = None
