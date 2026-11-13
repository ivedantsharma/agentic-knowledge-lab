from dataclasses import dataclass

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
)

_K_TO_ACTION = {
    1: RetrievalPolicyAction.SEARCH_HYBRID_K1,
    2: RetrievalPolicyAction.SEARCH_HYBRID_K2,
    3: RetrievalPolicyAction.SEARCH_HYBRID_K3,
    5: RetrievalPolicyAction.SEARCH_HYBRID_K5,
}


@dataclass(frozen=True)
class BudgetPolicyLabel:
    action: RetrievalPolicyAction
    minimal_k: int
    max_recall: float
    recall_by_k: dict[int, float]


def label_budget_policy(
    ranked_ids: list[str],
    supporting_ids: set[str],
    candidate_ks: tuple[int, ...] = (
        1,
        2,
        3,
        5,
    ),
) -> BudgetPolicyLabel:
    if not supporting_ids:
        raise ValueError(
            "supporting_ids must not be empty"
        )

    unsupported_ks = [
        k
        for k in candidate_ks
        if k not in _K_TO_ACTION
    ]
    if unsupported_ks:
        raise ValueError(
            "unsupported candidate k values: "
            f"{unsupported_ks}"
        )

    recall_by_k = {
        k: (
            len(
                set(ranked_ids[:k])
                & supporting_ids
            )
            / len(supporting_ids)
        )
        for k in candidate_ks
    }

    max_recall = max(
        recall_by_k.values()
    )
    minimal_k = min(
        k
        for k, recall
        in recall_by_k.items()
        if recall == max_recall
    )

    return BudgetPolicyLabel(
        action=_K_TO_ACTION[minimal_k],
        minimal_k=minimal_k,
        max_recall=max_recall,
        recall_by_k=recall_by_k,
    )
