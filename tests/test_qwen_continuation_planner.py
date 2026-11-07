from knowledge_engine.agent.qwen_continuation_planner import (
    QwenContinuationPlanner,
)


def test_answerability_parser_accepts_yes_no_shape() -> None:
    planner = object.__new__(
        QwenContinuationPlanner
    )

    planner._generate = lambda _instruction: "YES"

    assert planner.is_answerable(
        "Question?",
        "Evidence.",
    ) is True

    planner._generate = lambda _instruction: "NO"

    assert planner.is_answerable(
        "Question?",
        "Evidence.",
    ) is False


def test_generate_next_query_returns_model_text() -> None:
    planner = object.__new__(
        QwenContinuationPlanner
    )

    planner._generate = (
        lambda _instruction:
        "Where are exhausted Cirrus jobs sent?"
    )

    query = planner.generate_next_query(
        "Where are failed jobs sent?",
        "Cirrus handles production jobs.",
    )

    assert query == "Where are exhausted Cirrus jobs sent?"


def test_grounded_answer_requires_evidence_span() -> None:
    evidence = (
        "Jobs that exhaust retries are sent to the "
        "CIRRUS-DLQ dead-letter queue."
    )

    assert QwenContinuationPlanner.is_grounded_answer(
        "CIRRUS-DLQ dead-letter queue",
        evidence,
    )

    assert not QwenContinuationPlanner.is_grounded_answer(
        "the developer's own platform",
        evidence,
    )


def test_extract_or_abstain_returns_none_for_insufficient() -> None:
    planner = object.__new__(
        QwenContinuationPlanner
    )

    planner._generate = (
        lambda _instruction: "INSUFFICIENT"
    )

    result = planner.extract_or_abstain(
        "Where are failed jobs sent?",
        "Developer Productivity maintains Cirrus.",
    )

    assert result is None


def test_extract_or_abstain_returns_exact_span() -> None:
    planner = object.__new__(
        QwenContinuationPlanner
    )

    planner._generate = (
        lambda _instruction: "CIRRUS-DLQ"
    )

    result = planner.extract_or_abstain(
        "Where are failed jobs sent?",
        (
            "Jobs that exhaust retries are sent to "
            "CIRRUS-DLQ."
        ),
    )

    assert result == "CIRRUS-DLQ"
