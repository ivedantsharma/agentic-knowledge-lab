# Phase 5 — Why Add a Chunk Level?

## Sections are not always small

A section is semantically meaningful, but real sections may still contain hundreds or thousands of tokens.

If retrieval stops at the section level:

```text
correct section
→ large context block
→ downstream model
```

we may waste context on unrelated sentences.

## Three-level retrieval

```text
Document
→ Section
→ Chunk
```

uses structure for navigation and chunks for final evidence precision.

## The important distinction from flat chunk retrieval

Flat:

```text
query
→ every chunk in corpus
```

Hierarchical:

```text
query
→ promising documents
→ promising sections
→ chunks only inside those sections
```

The second approach restricts the expensive fine-grained search to a much smaller region.

## New risk

Every extra level creates another place where evidence can be lost.

Therefore we must measure evidence retention after each descent:

```text
parent survives?
section survives?
chunk survives?
```

A hierarchy is useful only if the context savings do not destroy recall.
