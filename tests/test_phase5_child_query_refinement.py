from scripts.run_phase5_child_query_refinement import (
    refine_child_query,
)


def test_refine_child_query_focuses_known_relations() -> None:
    assert refine_child_query(
        "What is the current Atlas signing-key identifier?"
    ) == "current signing-key identifier"

    assert refine_child_query(
        "How often do Borealis incremental backups run?"
    ) == "incremental backup cadence"

    assert refine_child_query(
        "Where are Cirrus jobs sent after exhausting all retries?"
    ) == "destination after all retry attempts"


def test_refine_child_query_preserves_unknown_question() -> None:
    question = "Which region hosts the service?"

    assert refine_child_query(question) == question