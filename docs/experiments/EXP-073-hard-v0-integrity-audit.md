# EXP-073: KnowledgeBench v2 Hard-v0 Integrity Audit

## Research question

Is the hard benchmark structurally valid enough to serve as a stable evaluation artifact?

## Motivation

Retrieval difficulty is not sufficient.

A benchmark can produce interesting scores while still containing annotation defects such as:

- missing document references,
- duplicate IDs,
- malformed temporal examples,
- ambiguity tasks with only one plausible interpretation.

Before Phase 7 closeout, these properties should be checked explicitly.

## Audit checks

The audit validates:

- duplicate document IDs,
- duplicate task IDs,
- every evidence-role reference resolves to a real document,
- answerable/unanswerable counts,
- per-challenge task counts,
- temporal tasks reference dated supporting/stale evidence,
- ambiguity tasks contain at least two competing candidates.

## Why this is not a model experiment

No retriever is run.

The only variable under test is benchmark integrity.

This separates:

```text
benchmark quality
from
model quality
```

## Success criterion

```text
passed=True
```

with no missing references, duplicates, temporal annotation failures, or malformed ambiguity tasks.

## Limitation

Passing the audit proves structural consistency, not semantic correctness of every annotation.

Human review and broader datasets remain future work.
