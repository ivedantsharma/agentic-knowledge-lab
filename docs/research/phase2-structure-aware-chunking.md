# Phase 2 — Structure-Aware Chunking

## Problem with fixed-size chunks

Fixed-size chunking knows nothing about document meaning.

It can cut:

```text
Token Rotation. Access-token signing
| CHUNK BOUNDARY |
keys rotate every 24 hours ...
```

The split is mechanically valid but semantically poor.

## Structure-aware idea

Many documents already contain useful boundaries:

- headings,
- sections,
- paragraphs,
- chapters,
- list items,
- HTML elements,
- Markdown headings.

Instead of choosing boundaries only by word count, preserve these structures.

For our synthetic manuals, headings are embedded as short labels such as:

```text
Authentication Overview.
Token Rotation.
Cache Behavior.
Deployment Notes.
```

We will explicitly represent sections in the next corpus version rather than trying to guess headings from punctuation.

## New representation

A structured source document can contain:

```text
document
  section 0
    title
    text
  section 1
    title
    text
```

Each section becomes one retrieval chunk initially.

Later, very large sections can still be subdivided.

## Hypothesis

Section-aware chunks should:
- preserve local topic context,
- avoid arbitrary evidence splits,
- create fewer redundant chunks than overlap,
- improve answer-bearing rank.

## Fair comparison

We will compare structure-aware chunks against our fixed-size baselines using the same:
- source information,
- questions,
- dense embedding model,
- evaluator,
- evidence-based relevance derivation.
