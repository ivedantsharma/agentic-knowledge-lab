# EXP-067: KnowledgeBench v2 Adversarial Role-Rank Diagnostic

## Research question

Are the stale, contradictory, and distractor documents in the v2 seed genuinely competitive retrieval candidates, or do top-k metrics hide that they rank too low to stress the retrievers?

## Motivation

EXP-066 produced:

```text
StaleHitRate=0.0000
ContradictionHitRate=0.0000
```

for both BM25 and Dense at top-3.

That can mean two very different things:

1. the retrievers successfully avoid misleading evidence, or
2. the benchmark's adversarial evidence is too weak to enter the candidate set.

Those interpretations cannot be separated by top-3 metrics alone.

## Controlled diagnostic

Do not change:

- corpus,
- tasks,
- BM25,
- MiniLM,
- scoring functions.

Change only the reporting depth:

```text
top-3
→ full-corpus ranking
```

For each task, print the exact rank of:

- supporting documents,
- distractors,
- contradictory documents,
- stale documents.

## Interpretation

If stale or contradictory evidence ranks 4th, the task is close to stressing top-3 retrieval.

If it ranks near the bottom, the adversarial document is likely too weak and the benchmark should be strengthened rather than declaring success.

## Why this matters

A hard benchmark should create meaningful competition between:

```text
correct evidence
vs
plausible but wrong evidence
```

The goal is not to make every adversarial document rank first.

The goal is to ensure the benchmark can expose tradeoffs and failure modes at realistic candidate budgets.
