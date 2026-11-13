from collections import Counter, defaultdict

from knowledge_engine.training.measured_policy_dataset import (
    MeasuredPolicyExample,
)


def balanced_oversample(
    examples: list[MeasuredPolicyExample],
) -> list[MeasuredPolicyExample]:
    if not examples:
        return []

    by_action: dict[
        str,
        list[MeasuredPolicyExample],
    ] = defaultdict(list)

    for example in examples:
        by_action[
            example.target_action.value
        ].append(example)

    max_count = max(
        len(group)
        for group in by_action.values()
    )

    balanced = []

    for action in sorted(by_action):
        group = by_action[action]

        for index in range(max_count):
            balanced.append(
                group[index % len(group)]
            )

    return balanced


def action_counts(
    examples: list[MeasuredPolicyExample],
) -> dict[str, int]:
    return dict(
        Counter(
            example.target_action.value
            for example in examples
        )
    )
