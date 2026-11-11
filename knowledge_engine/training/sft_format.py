from dataclasses import dataclass

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
)


@dataclass(frozen=True)
class PolicySFTText:
    system_text: str
    user_text: str
    target_text: str


def build_policy_sft_text(
    question: str,
    target_action: RetrievalPolicyAction,
) -> PolicySFTText:
    allowed = ", ".join(
        action.value
        for action in RetrievalPolicyAction
    )

    system_text = (
        "You are a retrieval-policy classifier. "
        "Return exactly one allowed action token and "
        "nothing else."
    )

    user_text = (
        "Choose the retrieval action for the query.\n"
        "Action meanings:\n"
        "SEARCH_HYBRID_K1 = retrieve 1 candidate.\n"
        "SEARCH_HYBRID_K2 = retrieve 2 candidates.\n"
        "SEARCH_HYBRID_K3 = retrieve 3 candidates.\n"
        "SEARCH_HYBRID_K5 = retrieve 5 candidates.\n"
        "REFORMULATE = the query needs decomposition or "
        "rewriting before more retrieval.\n"
        f"Allowed actions: {allowed}\n"
        f"Query: {question}"
    )

    return PolicySFTText(
        system_text=system_text,
        user_text=user_text,
        target_text=target_action.value,
    )


def build_target_only_labels(
    input_ids: list[int],
    prompt_token_count: int,
) -> list[int]:
    if prompt_token_count < 0:
        raise ValueError(
            "prompt_token_count must be non-negative"
        )

    if prompt_token_count > len(input_ids):
        raise ValueError(
            "prompt_token_count exceeds input length"
        )

    return (
        [-100] * prompt_token_count
        + input_ids[prompt_token_count:]
    )


def count_supervised_tokens(
    labels: list[int],
) -> int:
    return sum(
        label != -100
        for label in labels
    )
