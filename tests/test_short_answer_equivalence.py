from knowledgebench.evaluation.short_answer_equivalence import (
    canonicalize_short_answer,
    short_answers_equivalent,
)


def test_number_words_are_canonicalized() -> None:
    assert canonicalize_short_answer(
        "every twelve hours"
    ) == "12 hours"


def test_numeric_and_word_duration_are_equivalent() -> None:
    assert short_answers_equivalent(
        "10 minutes",
        "ten minutes",
    ) is True


def test_count_without_times_is_equivalent() -> None:
    assert short_answers_equivalent(
        "5",
        "five times",
    ) is True


def test_different_values_are_not_equivalent() -> None:
    assert short_answers_equivalent(
        "two minutes",
        "ten minutes",
    ) is False
