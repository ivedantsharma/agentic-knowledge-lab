# Phase 3 — Structured Retrieval State

## Why a single string is insufficient

Our previous state was:

```text
previous_fact = "Borealis"
```

But the evidence contained more useful information:

```text
entity: Borealis
qualifier: production
source: org_platform_reliability
evidence: Platform Reliability maintains ...
```

Compressing all of that into one string caused ambiguity later.

## New representation

We now introduce:

```text
RetrievalState
├── entity
├── qualifiers
├── source_document_id
└── evidence_text
```

This is still intentionally small.

It teaches an important agentic-search idea:

> State should preserve information that may affect later decisions.

## Controlled experiment

Hop 2 will independently extract:

```text
entity = Borealis
qualifier = production
```

Then hop 3 renders:

```text
What is the incremental backup cadence for the
{qualifier} {entity} service?
```

to:

```text
What is the incremental backup cadence for the
production Borealis service?
```

The qualifier is no longer hard-coded into the rendered query.

## What remains benchmark-provided?

We still provide:

- query templates,
- extraction regexes,
- hop count.

So Phase 3 remains deterministic.

The purpose is to understand state propagation before Phase 4 introduces autonomous planning and model-generated actions.
