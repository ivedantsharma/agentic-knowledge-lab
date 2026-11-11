# EXP-094: Query Feature Diagnostic for Retriever Routing

## Research question

What query-visible features correlate with the per-task retriever winners observed in EXP-093?

## Motivation

EXP-093 established modest routing headroom:

```text
best fixed Supporting Recall@3=0.7778
oracle Supporting Recall@3=0.8333
```

Before implementing a routing policy, inspect features available at inference time.

## Important constraint

Do not use:

- challenge labels,
- supporting-document IDs,
- evidence-chain annotations,
- expected answers,
- oracle winner labels as router inputs.

Those are benchmark-side supervision, not information available to a deployed router.

## Initial query features

### Token count

A crude query-complexity proxy.

### Capitalized-token count

A weak proxy for explicitly named entities.

### Temporal-cue count

Counts terms such as:

- current,
- latest,
- production,
- previous,
- pending.

### Relational-phrase count

Counts phrases such as:

- maintained by,
- operates,
- team that,
- service maintained by,
- system maintained by.

### Explicit-current cue

Whether the query explicitly says `current`.

### Multi-relation proxy

True when at least two relational phrases appear.

## Why this is diagnostic only

These features are not yet a routing policy.

EXP-094 prints them next to the observed EXP-093 winners so we can inspect whether any plausible routing rule exists.

If no meaningful pattern appears, we should not force a hand-written router.

## Next decision

After observing EXP-094:

- if simple features separate winner types, test a rule router;
- if not, expand the routing benchmark or use semantic query representations;
- do not train a learned router on six answerable tasks.
