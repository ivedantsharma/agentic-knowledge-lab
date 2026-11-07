# EXP-034: Relation-Alignment Verifier Probe

## Motivation

Exact-span grounding failed to reject:

```text
Cirrus
```

because the candidate is literally present in the evidence.

The missing property is relation alignment.

## Research question

Can Qwen2.5-0.5B-Instruct distinguish a grounded-but-relation-wrong answer from a grounded-and-correct answer?

## Probe cases

### Wrong candidate 1

```text
candidate = Cirrus
evidence = organization document
```

Expected:

```text
NO
```

### Wrong candidate 2

```text
candidate = Developer Productivity
```

Expected:

```text
NO
```

### Correct candidate

```text
candidate = CIRRUS-DLQ
evidence = final Cirrus manual
```

Expected:

```text
YES
```

### Correct longer span

```text
candidate = CIRRUS-DLQ dead-letter queue
```

Expected:

```text
YES
```

## Why probe before integration?

If Qwen cannot reliably verify relation alignment, adding it as another planner gate only adds complexity without improving correctness.

The verifier must demonstrate the capability independently first.
