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
