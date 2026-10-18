# Phase 2 — What Is Chunking?

## Kid explanation

Imagine a 300-page textbook.

A search system could compare your question against the entire textbook, but the whole book contains too many unrelated ideas.

So we cut the book into smaller pieces.

Those pieces are chunks.

The challenge is that cutting in the wrong place can separate information that belongs together.

## Engineer explanation

A source document is usually too large and too semantically broad to use as one retrieval unit.

Chunking transforms:

```text
SourceDocument
↓
DocumentChunk[]
```

Each chunk becomes independently indexable.

That improves retrieval granularity but creates new failure modes.

### Failure mode: boundary split

Source:

```text
... The service authenticates requests using rotating keys.
The active key version is KV-104.

KV-104 expires every 24 hours ...
```

A bad chunk boundary may put the key identifier in one chunk and the explanation in another.

### Failure mode: lost context

Chunk:

```text
It expires every 24 hours.
```

Without document or section context, "it" may be meaningless.

### Failure mode: redundant overlap

Large overlaps can preserve context, but may return several nearly identical chunks and waste retrieval/context budget.

## Provenance

Every chunk must remember where it came from.

At minimum:

- source_document_id
- chunk_id
- chunk_index
- start/end position

Later we can add:

- section title
- page
- URL
- timestamp
- parent heading
- source version

Without provenance, retrieval evidence cannot be reliably cited or audited.

## First baseline

We start with a deliberately simple word-based chunker.

Parameters:

```text
chunk_size_words
overlap_words
```

Example:

```text
chunk_size = 5
overlap = 2

words:
A B C D E F G H I J

chunks:
A B C D E
D E F G H
G H I J
```

The stride is:

```text
stride = chunk_size - overlap
```

This baseline is intentionally naive.

Its purpose is to give us something measurable that later chunking strategies must beat.
