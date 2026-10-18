# Phase 2 — Rich Chunk-Specific Context

## Parent context was helpful but incomplete

Adding:

```text
Document: Cirrus Worker Manual.
Section: Dead Letter Handling.
```

improved the relevant section from rank 3 to rank 2.

But the context still says very little about the relationship between the section and the rest of the document.

## Rich chunk context

A better contextual prefix can explain the role of the section.

Example:

```text
This section of the Cirrus Worker Manual describes what happens to jobs after all retry attempts fail.
```

Then the full retrieval text becomes:

```text
This section of the Cirrus Worker Manual describes what happens to jobs after all retry attempts fail.

Dead Letter Handling.
A job that fails all retry attempts is moved to the dead-letter queue named CIRRUS-DLQ.
```

## Important rule

The context must not be derived from the benchmark query.

Otherwise we would leak evaluation information into the indexed corpus.

The context is attached to the chunk once at indexing time and reused for every query.

## Another important rule

For this baseline, the context should avoid directly adding the answer identifier.

For example, do not put:

```text
This section explains that failed jobs go to CIRRUS-DLQ.
```

because then the contextual prefix itself contains the answer.

Instead use:

```text
This section explains what happens after retries are exhausted.
```

## Why we are still not using an LLM

We first want to isolate the value of richer context itself.

If manually authored chunk context improves retrieval, then later using an LLM to generate that context becomes a justified automation step rather than an unexplained complication.
