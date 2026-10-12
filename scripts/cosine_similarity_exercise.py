from math import sqrt


def dot_product(a: list[float], b: list[float]) -> float:
    """Return the dot product of two equal-length vectors."""
    # TODO: implement this yourself.
    raise NotImplementedError


def magnitude(v: list[float]) -> float:
    """Return the Euclidean magnitude (length) of a vector."""
    # TODO: implement this yourself.
    raise NotImplementedError


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Return cosine similarity between two non-zero vectors."""
    # TODO: implement this yourself.
    raise NotImplementedError


def main() -> None:
    a = [1.0, 0.0]
    b = [0.9, 0.1]
    c = [0.0, 1.0]

    print("A vs B:", cosine_similarity(a, b))
    print("A vs C:", cosine_similarity(a, c))


if __name__ == "__main__":
    main()
