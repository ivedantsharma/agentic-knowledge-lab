import pytest
from pydantic import ValidationError

from knowledgebench.tasks.multihop_schema import (
    EvidenceHop,
    MultiHopTask,
)


def test_multihop_task_accepts_ordered_hops() -> None:
    task = MultiHopTask(
        task_id="mh-001",
        question="Who owns the service used by Atlas?",
        hops=[
            EvidenceHop(
                hop_index=0,
                query="Atlas dependency",
                expected_document_id="doc-atlas",
                expected_fact="Borealis",
            ),
            EvidenceHop(
                hop_index=1,
                query="Borealis owner",
                expected_document_id="doc-borealis",
                expected_fact="Platform Team",
            ),
        ],
        expected_answer="Platform Team",
    )

    assert len(task.hops) == 2
    assert task.hops[1].expected_fact == "Platform Team"


def test_multihop_task_rejects_blank_question() -> None:
    with pytest.raises(ValidationError):
        MultiHopTask(
            task_id="mh-001",
            question="   ",
            hops=[],
            expected_answer="answer",
        )
