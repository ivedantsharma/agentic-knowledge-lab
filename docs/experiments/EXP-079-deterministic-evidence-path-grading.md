# EXP-079: Deterministic Evidence-Path Grading

## Research question

Can agent evaluation distinguish:

```text
all required evidence was eventually retrieved
```

from:

```text
the evidence dependency path was followed in the intended order
```

## Motivation

EXP-076 introduced set-based evidence coverage.

Set-based coverage ignores order.

For a multi-hop task:

```text
A → B → C
```

these traces have the same document set:

```text
A, B, C
C, A, B
```

but they do not represent the same reasoning trajectory.

## Gold path

The benchmark already provides ordered hops:

```text
task.hops
```

Therefore:

```text
expected_path =
[hop.expected_document_id for hop in task.hops]
```

## Metrics

### Path Coverage

Set-based fraction of gold path documents consumed.

### Ordered Path Complete

True when the gold document sequence appears as a subsequence of consumed evidence.

This allows extra searches while preserving dependency order.

### Exact Path Match

True only when:

```text
consumed_path == expected_path
```

### Extra Documents

Counts consumed documents outside the gold evidence path.

## Controlled setup

Keep fixed:

- Phase 4 benchmark,
- Phase 4 corpus,
- RuleBasedPlanner,
- SemanticPlanner,
- DenseSearchTool,
- trace recording.

Add only the evidence-path grader.

## Important interpretation

A perfect evidence path still does not guarantee a correct answer.

The semantic planner already demonstrates this on `ood-001`:

```text
correct evidence
but wrong relation selection
```

Therefore path quality is another independent evaluation axis.
