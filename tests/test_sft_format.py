import pytest

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
)
from knowledge_engine.training.sft_format import (
    build_policy_sft_text,
    build_target_only_labels,
    count_supervised_tokens,
)


def test_policy_sft_text_contains_query_and_target() -> None:
    formatted = build_policy_sft_text(
        question="How many retries does Cirrus use?",
        target_action=(
            RetrievalPolicyAction.SEARCH_HYBRID_K1
        ),
    )

    assert "Cirrus" in formatted.user_text
    assert (
        formatted.target_text
        == "SEARCH_HYBRID_K1"
    )


def test_target_only_labels_mask_prompt() -> None:
    labels = build_target_only_labels(
        input_ids=[10, 11, 12, 13, 14],
        prompt_token_count=3,
    )

    assert labels == [
        -100,
        -100,
        -100,
        13,
        14,
    ]
    assert count_supervised_tokens(labels) == 2


def test_target_only_labels_reject_invalid_length() -> None:
    with pytest.raises(ValueError):
        build_target_only_labels(
            input_ids=[1, 2],
            prompt_token_count=3,
        )
