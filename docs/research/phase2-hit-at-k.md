# Phase 2 — Why Recall@K Can Mislead with Overlapping Chunks

## The problem

Overlap can create multiple chunks containing the same evidence.

Example:

```text
relevant chunks:
chunk-0001
chunk-0002
```

If top-1 retrieves:

```text
chunk-0001
```

then ordinary Recall@1 is:

```text
1 / 2 = 0.5
```

But for the user-facing retrieval goal, the system succeeded:

> at least one answer-bearing chunk was retrieved at rank 1.

## Hit@K

Define:

```text
Hit@K = 1
```

if at least one relevant item appears in the top K.

Otherwise:

```text
Hit@K = 0
```

Across tasks:

```text
Mean Hit@K
=
fraction of tasks with at least one relevant result in top K
```

## Why both metrics matter

Recall@K asks:

> How much of all labeled evidence did I retrieve?

Hit@K asks:

> Did I retrieve at least one usable evidence unit?

For duplicated overlapping chunks, Hit@K is often the better primary success metric.

For multi-hop tasks where multiple distinct evidence pieces are all required, Recall@K becomes important again.

So Phase 2 should report both rather than replace one with the other.
