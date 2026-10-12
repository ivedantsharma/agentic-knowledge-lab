from scripts.cosine_similarity_exercise import cosine_similarity


def test_semantically_close_vectors_rank_higher() -> None:
    dog_like = [1.0, 0.0]
    puppy_like = [0.9, 0.1]
    finance_like = [0.0, 1.0]

    close_score = cosine_similarity(dog_like, puppy_like)
    far_score = cosine_similarity(dog_like, finance_like)

    assert close_score > far_score
