# EXP-016: Extracted-Fact Multi-Hop Chaining

## Goal

Remove gold intermediate facts from the execution loop.

Instead, extract the fact from the retrieved document and use it to render the next query.

## Result

```text
HopAccuracy      = 1.0000
ExactChainMatch  = 1.0000
FactAccuracy     = 1.0000
AnswerCorrect    = 1.0000
```

## Execution trace

### Hop 1

Query:

```text
Which team operates Atlas?
```

Retrieved:

```text
org_atlas
```

Extracted fact:

```text
Platform Reliability
```

### Hop 2

Rendered query:

```text
Which storage system is maintained by Platform Reliability?
```

Retrieved:

```text
org_platform_reliability
```

Extracted fact:

```text
Borealis
```

### Hop 3

Rendered query:

```text
What is the incremental backup cadence for Borealis?
```

Retrieved:

```text
manual_borealis
```

Extracted fact:

```text
every six hours
```

Final answer:

```text
every six hours
```

## Interpretation

The system now performs a real dependency chain:

```text
retrieval
→ extraction
→ query construction
→ retrieval
→ extraction
→ query construction
→ retrieval
→ extraction
```

The benchmark no longer provides the intermediate fact during execution.

## What is still benchmark-provided?

The benchmark still provides:

- the query templates,
- the extraction patterns,
- the number of hops,
- the stopping point.

So this is not yet autonomous planning.

## Next research question

How robust is this chain when the corpus becomes less clean?

We should now introduce:

- relation distractors,
- multiple similar entities,
- misleading lexical matches,
- extraction ambiguity.

This will test whether the pipeline succeeds because the current corpus is easy, or because the chaining architecture is robust.
