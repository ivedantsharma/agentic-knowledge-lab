from typing import Any

from pydantic import BaseModel, Field

from knowledge_engine.retrieval.state import RetrievalState


class PlannerTraceStep(BaseModel):
    step_index: int
    action_type: str
    query: str | None = None
    retrieved_document_id: str | None = None
    extracted_fact: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class PlannerState(BaseModel):
    question: str
    step_index: int = 0
    retrieval_state: RetrievalState = Field(
        default_factory=RetrievalState
    )
    trace: list[PlannerTraceStep] = Field(
        default_factory=list
    )
    final_answer: str | None = None
    stopped: bool = False
