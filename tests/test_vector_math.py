import pytest

from knowledge_engine.retrieval.vector_math import (
    cosine_similarity,
    dot_product,
    magnitude,
)


def test_dot_product() -> None:
    assert dot_product(
        [1.0, 2.0],
        [3.0, 4.0],
    ) == 11.0


def test_magnitude() -> None:
    assert magnitude(
        [3.0, 4.0]
    ) == 5.0


def test_cosine_similarity_identical_vectors() -> None:
    assert cosine_similarity(
        [1.0, 0.0],
        [1.0, 0.0],
    ) == pytest.approx(1.0)
