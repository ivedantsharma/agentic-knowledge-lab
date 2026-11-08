# Phase 5 — Retrieval Recall vs Context Efficiency

## Two objectives

Hierarchical retrieval should optimize both:

```text
1. preserve answer-bearing evidence
2. minimize downstream context
```

EXP-048 solves the first objective:

```text
EvidenceRetentionRate=1.0000
```

but not the second.

## Why overlap can increase context

With overlap:

```text
chunk 0: A B C D E F G H I J
chunk 1: H I J K L M N
```

naively returning both chunks sends:

```text
A B C D E F G H I J H I J K L M N
```

The overlap words are duplicated.

## Better representation

Instead of returning both raw chunks, merge their source ranges:

```text
start = min(start_word)
end   = max(end_word)
```

and reconstruct one unique local window from the source section.

That produces:

```text
A B C D E F G H I J K L M N
```

with the same evidence coverage and less context.

## Research principle

Retrieval candidates and returned context do not have to be identical.

Small overlapping chunks can be useful for ranking, while a deduplicated local window can be better for downstream consumption.
