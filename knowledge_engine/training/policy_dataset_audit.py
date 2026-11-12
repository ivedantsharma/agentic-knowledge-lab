from collections import defaultdict
from dataclasses import dataclass

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
    RetrievalPolicyExample,
    RetrievalPolicySplit,
)


@dataclass(frozen=True)
class ActionSourceSupport:
    action: RetrievalPolicyAction
    source_task_ids: tuple[str, ...]
    split_source_task_ids: dict[str, tuple[str, ...]]

    @property
    def source_count(self) -> int:
        return len(self.source_task_ids)

    @property
    def supports_source_disjoint_evaluation(self) -> bool:
        train_sources = set(
            self.split_source_task_ids.get(
                RetrievalPolicySplit.TRAIN.value,
                (),
            )
        )
        eval_sources = set(
            self.split_source_task_ids.get(
                RetrievalPolicySplit.DEV.value,
                (),
            )
        ) | set(
            self.split_source_task_ids.get(
                RetrievalPolicySplit.HELDOUT.value,
                (),
            )
        )

        return bool(
            train_sources
            and eval_sources
            and train_sources.isdisjoint(eval_sources)
        )


def audit_action_source_support(
    examples: list[RetrievalPolicyExample],
) -> list[ActionSourceSupport]:
    sources_by_action: dict[
        RetrievalPolicyAction,
        set[str],
    ] = defaultdict(set)

    split_sources_by_action: dict[
        RetrievalPolicyAction,
        dict[str, set[str]],
    ] = defaultdict(
        lambda: defaultdict(set)
    )

    for example in examples:
        action = example.target_action
        sources_by_action[action].add(
            example.source_task_id
        )

        if example.split is not None:
            split_sources_by_action[action][
                example.split.value
            ].add(
                example.source_task_id
            )

    results = []

    for action in RetrievalPolicyAction:
        split_mapping = {
            split: tuple(sorted(source_ids))
            for split, source_ids
            in split_sources_by_action[
                action
            ].items()
        }

        results.append(
            ActionSourceSupport(
                action=action,
                source_task_ids=tuple(
                    sorted(
                        sources_by_action[action]
                    )
                ),
                split_source_task_ids=(
                    split_mapping
                ),
            )
        )

    return results
