# EXP-061: Referent-First Entity-Type Cue Diagnostic

## Research question

Does using the earliest explicit entity-type cue repair the mixed-cue failures from EXP-060?

## Controlled comparison

Baseline:

```text
any cues from multiple types
→ abstain
```

Treatment:

```text
scan mention left to right
→ use earliest explicit type cue
```

Everything downstream remains fixed:

- same mentions,
- same graph,
- same MiniLM embeddings,
- same type-constrained semantic ranker,
- same threshold = 0.39.

## Motivation

Example:

```text
team operating the Atlas authentication service
^^^^                                  ^^^^^^^
referent type                         related object
```

The treatment encodes the hypothesis that the earlier type cue is more likely to describe the mention head in this synthetic benchmark.

## Metrics

- BaselineTypeInferenceAccuracy
- FirstCueTypeInferenceAccuracy
- BaselineResolvableEntityAccuracy
- FirstCueResolvableEntityAccuracy
- BaselineAbstentionAccuracy
- FirstCueAbstentionAccuracy

## Caveat

This is a diagnostic heuristic, not a general linguistic parser.

If it repairs the development failures, it must still be validated on new phrasing before adoption.
