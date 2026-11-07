# EXP-030: Model-Family Ablation for Planner Capabilities

## Motivation

FLAN-T5-small and FLAN-T5-base both failed open-ended search-query generation.

Increasing FLAN model capacity repaired answerability but did not repair query generation.

## Controlled comparison

The benchmark semantics remain unchanged.

We keep the same:

- original question,
- intermediate evidence,
- final evidence,
- five capability categories,
- deterministic decoding.

We change model family:

```text
FLAN-T5
→ Qwen2.5 Instruct
```

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

Unlike FLAN-T5's encoder-decoder interface, this is used as a causal chat model.

The prompt is supplied through the tokenizer's chat template so inference follows the model's instruction-tuning format.

## Probes

1. initial query generation,
2. next-query generation after intermediate evidence,
3. grounded answer extraction,
4. answerability without evidence,
5. answerability with sufficient evidence.

## Evaluation

Query generation is successful when the output is an information-seeking query that would retrieve evidence needed for the requested relation.

Exact wording is not required.

Expected semantic progression:

```text
Developer Productivity
→ identify Cirrus
→ ask where exhausted Cirrus jobs are sent
```

Answer extraction should contain:

```text
CIRRUS-DLQ
```

Answerability should produce:

```text
without evidence → NO
with final evidence → YES
```

## Interpretation

If Qwen succeeds where both FLAN variants failed, the planner bottleneck is not merely parameter count.

The interaction between model family, post-training, and instruction interface materially affects planner capability.
