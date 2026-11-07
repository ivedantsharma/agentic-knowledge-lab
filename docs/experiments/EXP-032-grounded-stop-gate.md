# EXP-032: Grounded STOP Gate

## Failure being addressed

The first hybrid planner run stopped after retrieving:

```text
Developer Productivity maintains the Cirrus worker platform...
```

It returned:

```text
Failed jobs are sent to the developer's own platform.
```

The evidence was relevant to the question but did not contain the requested destination.

This is a false-positive STOP.

## Key distinction

```text
relevant evidence
!=
sufficient evidence
```

A stopping policy should not terminate merely because the evidence is topically related.

## New rule

A STOP now requires two conditions.

### Condition 1 — model answerability

Qwen must classify the evidence as sufficient.

### Condition 2 — deterministic grounding

Qwen must extract the answer as an exact span copied from the evidence.

The extracted span must literally occur in the evidence after case/whitespace normalization.

Conceptually:

```text
Qwen says YES
↓
extract exact answer span
↓
is span present in evidence?
├── YES → STOP
└── NO  → reject stop and SEARCH
```

## Why use a deterministic grounding gate?

Language models can hallucinate plausible answers even when they claim evidence is sufficient.

A deterministic support check acts as a guardrail around the stochastic/model judgment.

## Expected effect on the OOD task

At the intermediate organization document:

```text
"developer's own platform"
```

is not an evidence span.

Therefore STOP should be rejected.

The planner should then generate another search query.

At the final Cirrus manual, a valid answer such as:

```text
CIRRUS-DLQ dead-letter queue
```

is directly present in the evidence, so STOP can be accepted.

## Limitation

Exact-span grounding is intentionally strict.

It can reject valid paraphrased answers.

For the current synthetic benchmark this is useful because answers are explicitly present in the evidence.

Later phases can use semantic or model-based groundedness graders.
