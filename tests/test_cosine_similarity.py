import pytest

from scripts.cosine_similarity_exercise import cosine_similarity, dot_product, magnitude


def test_dot_product() -> None:
    assert dot_product([1.0, 2.0], [3.0, 4.0]) == pytest.approx(11.0)


def test_magnitude() -> None:
    assert magnitude([3.0, 4.0]) == pytest.approx(5.0)


def test_cosine_similarity_similar_vectors() -> None:
    result = cosine_similarity([1.0, 0.0], [0.9, 0.1])
    assert result == pytest.approx(0.9938837347)


def test_cosine_similarity_perpendicular_vectors() -> None:
    result = cosine_similarity([1.0, 0.0], [0.0, 1.0])
    assert result == pytest.approx(0.0)
