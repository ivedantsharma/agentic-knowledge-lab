# Phase 4 — Generative Planning Still Needs Structured State

## A common misconception

Once a generative model is introduced, it is tempting to assume raw text evidence is enough.

EXP-037 shows that this is false.

The system had already extracted useful state:

```text
entity
qualifiers
source document
```

but the generative query planner did not receive these fields explicitly.

## Example: Meridian

State after the first hop:

```text
entity = Meridian
qualifier = production
```

Generated query:

```text
Meridian rotating signing keys
```

The word `production` disappeared.

That small omission changed retrieval ranking:

```text
development manual > production manual
```

and produced a wrong final answer.

## Example: Platform Reliability

State:

```text
entity = Platform Reliability
```

The original question requires:

```text
Atlas
→ Platform Reliability
→ storage system
→ backup cadence
```

The model instead jumped back to:

```text
Atlas backup cadence
```

and retrieved a distractor.

## Lesson

Generative planning does not replace state representation.

A better architecture is:

```text
raw evidence
+
structured state
+
original goal
→ next query
```

The structured state acts as a compact memory of what has already been learned.

## Phase 3 connection

Phase 3 already demonstrated:

```text
compressing state too aggressively
→ ambiguous next query
```

EXP-037 shows the same principle in an LLM planner:

```text
failing to expose structured state
→ lost entity / qualifier
→ unstable retrieval trajectory
```

This is a useful continuity between the deterministic and generative phases.
