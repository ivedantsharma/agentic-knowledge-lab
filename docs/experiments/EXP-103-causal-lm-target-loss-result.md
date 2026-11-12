# EXP-103 Result: Causal-LM Target-Only Loss Mechanics

## Validation

```text
261 tests passed
ruff passed
```

## Result

```text
prompt_tokens=168
full_tokens=177
supervised_tokens=9
masked_prompt_tokens=168
supervised_decode='SEARCH_HYBRID_K5<|im_end|>\n'

target_only_loss=0.204247
unmasked_full_sequence_loss=3.519113
```

## Interpretation

The target-only masking boundary is correct.

The prompt occupies 168 tokens and is masked with label `-100`.

Only the nine-token assistant suffix contributes to the supervised loss.

The decoded supervised suffix contains the intended retrieval action and assistant termination token.

The masked and unmasked loss values optimize different token sets and are not directly comparable as quality metrics.

## Decision

The preprocessing path is ready for a real parameter-update experiment.

Use parameter-efficient fine-tuning first rather than full-model optimization.
