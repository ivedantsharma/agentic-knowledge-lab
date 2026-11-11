# EXP-101: Frozen Retrieval Policy Baseline

## Research question

How well does the frozen Qwen2.5-0.5B-Instruct model choose Phase 10 retrieval-policy actions before supervised fine-tuning?

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

## Seed dataset

Six Phase 10 answerable hard tasks with oracle-derived actions.

Action vocabulary:

```text
SEARCH_HYBRID_K1
SEARCH_HYBRID_K2
SEARCH_HYBRID_K3
SEARCH_HYBRID_K5
REFORMULATE
```

## Controlled protocol

- no weight updates,
- deterministic decoding,
- exact action-token parser,
- same instruction for all examples.

## Metrics

### Format compliance

Fraction of outputs that exactly parse as one allowed action.

### Action accuracy

Fraction exactly matching the oracle-derived target action.

### Prediction distribution

Counts of each predicted action.

This detects degenerate behavior such as predicting the same action for every query.

## Interpretation

High format compliance but low action accuracy means the model understands the protocol but not the retrieval policy.

Low format compliance means output protocol learning itself is part of the fine-tuning problem.

A high baseline on six examples would not establish generalization.

## Next step

After EXP-101:

1. expand the policy demonstration dataset,
2. create train/dev/heldout splits,
3. learn PyTorch loss/token masking mechanics,
4. run the first supervised fine-tuning experiment.
