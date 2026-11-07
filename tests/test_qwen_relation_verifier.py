from knowledge_engine.agent.qwen_relation_verifier import (
    QwenRelationVerifier,
)


def test_relation_verifier_accepts_yes() -> None:
    verifier = object.__new__(
        QwenRelationVerifier
    )

    verifier._generate = lambda _instruction: "YES"

    assert verifier.verify(
        "Where are jobs sent?",
        "Jobs are sent to CIRRUS-DLQ.",
        "CIRRUS-DLQ",
    ) is True


def test_relation_verifier_rejects_no() -> None:
    verifier = object.__new__(
        QwenRelationVerifier
    )

    verifier._generate = lambda _instruction: "NO"

    assert verifier.verify(
        "Where are jobs sent?",
        "Developer Productivity maintains Cirrus.",
        "Cirrus",
    ) is False
