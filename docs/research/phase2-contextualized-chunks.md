# Phase 2 — Deterministic Contextualized Chunks

## Motivation

Our section-aware chunker preserved semantic boundaries but still failed to rank the Cirrus answer-bearing section first.

The relevant section was:

```text
Dead Letter Handling.
A job that fails all retry attempts is moved to the dead-letter queue named CIRRUS-DLQ.
```

The query included:

```text
Cirrus jobs
exhausting all retries
```

The section contained the retry/answer semantics, but did not explicitly contain the parent document identity "Cirrus Worker Manual".

## Contextual retrieval idea

A chunk can be easier to retrieve if we prepend concise parent context.

Example:

```text
Document: Cirrus Worker Manual.
Section: Dead Letter Handling.

A job that fails all retry attempts is moved to the dead-letter queue named CIRRUS-DLQ.
```

Now the retrieval unit contains:
- document identity,
- section identity,
- answer-bearing text.

## Important distinction

Anthropic's Contextual Retrieval uses chunk-specific context generated from the whole document.

This Phase 2 baseline is simpler.

We use deterministic metadata already present in the corpus:

- document title,
- section title.

This isolates whether adding parent context helps retrieval before introducing LLM-generated contextualization.

## Hypothesis

Contextualized section chunks should improve retrieval when:
- local section text lacks document identity,
- the query refers to the parent document/entity,
- section-level content is otherwise correct.

## Controlled comparison

Compare:

1. plain section chunks,
2. contextualized section chunks.

Keep fixed:
- section boundaries,
- source text,
- dense model,
- evidence labels,
- top-k,
- evaluator.

The only changed variable is the added context prefix.
