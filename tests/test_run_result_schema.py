import pytest
from pydantic import ValidationError

from knowledgebench.runs.schema import RunResult


def test_valid_run_result() -> None:
    result = RunResult(
        task_id="kb-001",
        generated_answer="Company Y",
        retrieved_document_ids=["doc-12", "doc-47"],
        tool_calls=2,
        latency_ms=145.5,
        metadata={"model": "example-model"},
    )

    assert result.task_id == "kb-001"
    assert result.tool_calls == 2
    assert result.latency_ms == pytest.approx(145.5)


def test_task_id_is_trimmed() -> None:
    result = RunResult(task_id="   kb-001   ")

    assert result.task_id == "kb-001"


def test_blank_task_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        RunResult(task_id="   ")


def test_negative_tool_calls_are_rejected() -> None:
    with pytest.raises(ValidationError):
        RunResult(task_id="kb-001", tool_calls=-1)


def test_negative_latency_is_rejected() -> None:
    with pytest.raises(ValidationError):
        RunResult(task_id="kb-001", latency_ms=-0.1)


def test_empty_retrieval_and_missing_answer_are_allowed() -> None:
    result = RunResult(task_id="kb-002")

    assert result.generated_answer is None
    assert result.retrieved_document_ids == []
    assert result.tool_calls == 0
    assert result.latency_ms is None
    assert result.metadata == {}
