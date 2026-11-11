# EXP-101 Result: Frozen Retrieval Policy Baseline

## Validation

```text
258 tests passed
ruff passed
```

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

## Results

```text
format_compliance=1.0000
action_accuracy=0.0000
predicted_counts={
  'SEARCH_HYBRID_K3': 5,
  'SEARCH_HYBRID_K2': 1
}
```

## Interpretation

The frozen model understands the output protocol but not the retrieval policy.

It produced a valid action token for every example.

However, none matched the oracle-derived target.

The model also shows a strong default-action bias toward:

```text
SEARCH_HYBRID_K3
```

This is useful because it separates two learning problems:

```text
format learning
vs
policy learning
```

Format learning is already solved in this probe.

The main Phase 11 objective is therefore to teach query-to-action mapping.

## Decision

Do not tune prompts further.

Expand the supervised dataset, establish splits, then fine-tune and compare against this frozen baseline.
