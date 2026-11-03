from math import sqrt


def dot_product(
    a: list[float],
    b: list[float],
) -> float:
    """Return the dot product of equal-length vectors."""
    if len(a) != len(b):
        raise ValueError(
            "Vectors must have the same length"
        )

    return sum(
        x * y
        for x, y in zip(a, b)
    )


def magnitude(v: list[float]) -> float:
    """Return the Euclidean magnitude of a vector."""
    return sqrt(
        sum(x**2 for x in v)
    )


def cosine_similarity(
    a: list[float],
    b: list[float],
) -> float:
    """Return cosine similarity for two vectors."""
    dot = dot_product(a, b)
    mag_a = magnitude(a)
    mag_b = magnitude(b)

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)
