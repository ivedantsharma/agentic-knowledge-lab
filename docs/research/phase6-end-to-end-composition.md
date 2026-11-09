# Phase 6: End-to-End Graph QA Composition

A research system should be evaluated both component-wise and end-to-end.

Phase 6 first isolated:

```text
graph representation
traversal
entity linking
semantic entity ranking
type constraints
path selection
```

This made failures attributable.

Only after those components were understood do we compose them.

## Why composition can still fail

Even if every component performs well independently, integration can expose:

- incompatible assumptions,
- representation mismatches,
- error propagation,
- missing provenance,
- incorrect handoff between stages.

## Current composition

```text
question
→ exact/alias entity linker
→ structurally valid path enumeration
→ semantic path ranking
→ deterministic claim traversal
→ answer + provenance
```

## Remaining structural limitation

The current traversal requires exactly one claim for each:

```text
(subject entity, relation)
```

Real knowledge graphs often contain multiple valid claims distinguished by qualifiers:

```text
Borealis
  backup cadence
    production → every six hours
    staging    → every twelve hours
```

Phase 6 is not complete until this ambiguity is treated as an explicit research variable rather than silently ignored.
