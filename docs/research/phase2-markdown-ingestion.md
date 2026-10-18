# Phase 2 — Markdown Ingestion

## Why Markdown first?

Markdown is a good first real file format because it already exposes useful semantic structure:

```text
# document title
## section
### subsection
```

That structure maps naturally to our `StructuredDocument` model.

It is also easy to inspect and test.

## Goal

Convert:

```text
manual.md
↓
Markdown parser
↓
StructuredDocument
↓
DocumentSection[]
↓
section/context chunking
↓
retrieval
```

## Baseline parser

For Phase 2 we support:

- first level-1 heading as document title,
- level-2/3 headings as sections,
- paragraph text under each heading,
- metadata containing source path and title.

We deliberately do not yet support:

- tables,
- nested lists as special structures,
- code-block semantics,
- front matter,
- HTML,
- footnotes.

Those can be added later if experiments justify them.

## Why not add a Markdown library immediately?

Because our needs are intentionally narrow.

A tiny parser makes the transformation logic explicit:

```text
heading
→ section boundary

body lines
→ section text
```

Once requirements grow, replacing this with a full parser becomes straightforward.

## Provenance

Every ingested document should remember:

- source path,
- parsed document title,
- section title.

That means a retrieved chunk can be traced back to the file it came from.
