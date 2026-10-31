from scripts.run_phase3_gold_fact_chaining import (
    render_query,
)


def test_render_query_substitutes_previous_fact() -> None:
    assert render_query(
        "Who maintains {previous_fact}?",
        "Borealis",
    ) == "Who maintains Borealis?"


def test_render_query_without_placeholder() -> None:
    assert render_query(
        "Which team operates Atlas?",
        None,
    ) == "Which team operates Atlas?"
