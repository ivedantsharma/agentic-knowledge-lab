# Phase 4 — What the Qwen Probe Changes

## The important result

The Qwen probe produced:

```text
Where do failed jobs go after they have been exhausted?
```

after intermediate evidence.

This is qualitatively different from the FLAN outputs.

FLAN produced statements such as:

```text
Developer Productivity maintains the Cirrus worker platform...
```

Qwen produced an information-seeking query.

That means it represented the missing information as a question.

## Bootstrap planning vs continuation planning

The probe exposed two different planner problems.

### Bootstrap planning

At step zero, the system has:

```text
original question
no retrieved evidence
no current entity
```

The model must decide where to begin.

Qwen returned:

```text
failed jobs
```

This is too vague for reliable retrieval.

### Continuation planning

After one retrieval, the system has:

```text
entity = Cirrus
qualifier = production
evidence = Developer Productivity maintains Cirrus...
```

Now Qwen generated:

```text
Where do failed jobs go after they have been exhausted?
```

That is much stronger.

## Why this matters

Agent planning is not one homogeneous skill.

The first action may require entity/link discovery.

Later actions can use structured state to formulate a targeted query.

This suggests we should evaluate:

```text
initial planning quality
continuation planning quality
stopping quality
answer extraction quality
```

separately.

## Next architecture

We can now justify a hybrid baseline:

1. deterministic or semantic bootstrap for the first hop,
2. Qwen for open-ended continuation queries,
3. Qwen for answerability,
4. Qwen for grounded final extraction.

This is not a hack.

It is a modular planner where each component owns the capability it has demonstrated experimentally.
