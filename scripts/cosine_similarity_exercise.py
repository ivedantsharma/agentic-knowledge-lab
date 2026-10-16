from math import sqrt


def dot_product(a: list[float], b: list[float]) -> float:
    """Return the dot product of two equal-length vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    return sum(x * y for x, y in zip(a, b))


def magnitude(v: list[float]) -> float:
    """Return the Euclidean magnitude (length) of a vector."""
    return sqrt(sum(x ** 2 for x in v))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Return cosine similarity between two non-zero vectors."""
    dot_prod = dot_product(a, b)
    mag_a = magnitude(a)
    mag_b = magnitude(b)
    return dot_prod / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0


def main() -> None:
    a = [1.0, 0.0]
    b = [0.9, 0.1]
    c = [0.0, 1.0]

    print("A vs B:", cosine_similarity(a, b))
    print("A vs C:", cosine_similarity(a, c))


if __name__ == "__main__":
    main()
