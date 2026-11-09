# EXP-065: KnowledgeBench v2 Task Taxonomy and Seed Dataset

## Research question

Can we encode hard knowledge-retrieval cases so that benchmark failures are attributable to specific challenge types rather than collapsing into one accuracy number?

## Why Phase 7 starts with schemas

A hard benchmark needs more than:

```text
question
→ relevant document
```

The same task may contain:

- documents required for the answer,
- plausible distractors,
- stale evidence,
- contradictory evidence,
- multiple hops,
- no answer at all.

Without explicit labels, later evaluation cannot distinguish these failure modes.

## Challenge taxonomy

The initial taxonomy is:

```text
multi_hop
distractor
ambiguity
contradiction
stale_knowledge
unanswerable
```

These labels can be combined.

A task such as:

```text
Atlas → Platform Reliability → Borealis → backup cadence
```

can simultaneously be:

```text
multi_hop
+ distractor
+ stale_knowledge
```

## Ground-truth roles

Each task separates document roles:

### supporting_document_ids

Documents that support the intended answer.

### evidence_chain

Ordered documents needed for compositional retrieval.

This is stricter than an unordered relevant set.

### distractor_document_ids

Plausible but irrelevant evidence.

### contradicting_document_ids

Evidence that appears to disagree with the answer.

A contradiction may be resolved by provenance, authority, status, or context.

### stale_document_ids

Evidence that was previously valid but should not determine the current answer.

## Unanswerable tasks

A task with:

```text
should_answer=False
```

must:

- include the `unanswerable` challenge label,
- have no expected answer,
- have no supporting documents.

This prevents accidental answer leakage in the benchmark definition.

## Seed dataset

The first v2 seed contains three tasks:

1. multi-hop + distractor + stale knowledge,
2. multi-hop + contradiction,
3. unanswerable.

This is a schema-mechanics dataset, not the final Phase 7 benchmark.

## What EXP-065 proves

If validation passes, it proves only that:

- the taxonomy is representable,
- invalid task combinations are rejected,
- document roles are explicit,
- the seed dataset can support later hard-evaluation work.

It does not yet measure retrieval quality.
