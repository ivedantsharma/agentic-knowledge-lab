# EXP-100: Qualifier-Preserving Query Transformation

## Research question

Does explicitly preserving temporal and deployment qualifiers improve decomposed multi-hop retrieval?

## Trigger from EXP-099

Oracle decomposition improved the hard Helios task, but it still retrieved stale evidence.

The transformed query:

```text
What cache duration does production Solstice use?
```

ranked the stale Solstice policy above the current one.

## Hypothesis

Multi-hop query transformation can lose important constraints from the original question.

Examples:

- current,
- production,
- service type,
- relation context.

If those qualifiers are carried into each focused query, retrieval should better preserve the intended evidence path.

## Controlled variable

Keep fixed:

- corpus,
- Hybrid RRF,
- MiniLM,
- top-1 per transformed query,
- task set.

Compare:

```text
baseline oracle decomposition
vs
qualifier-preserving oracle decomposition
```

## Tasks

- kbv2-hard-001,
- kbv2-hard-005,
- kbv2-hard-006.

## Metrics

Per task:

- retrieved union,
- supporting-document recall.

Aggregate:

- mean recall.

## Interpretation

A positive result would show that query transformation quality is not only about decomposition.

It must also preserve task state and qualifiers across hops.

This connects Phase 10 directly back to the structured retrieval-state lessons from Phase 3.
