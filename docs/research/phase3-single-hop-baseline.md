# Phase 3 — Single-Hop Baseline

## What is the baseline?

Take the full multi-hop question and send it to the retriever once.

```text
question
↓
one dense search
↓
ranked documents
```

No decomposition.
No intermediate facts.
No query rewriting.

## Why build a deliberately limited baseline?

Research needs a comparison point.

If we immediately build a multi-step system and it works, we cannot tell whether multiple hops were actually necessary.

So first ask:

> How well does ordinary one-shot retrieval do?

## What should we inspect?

For each task:

- where does hop-1 evidence rank?
- where does hop-2 evidence rank?
- where does final-answer evidence rank?
- do distractors rank above required evidence?

The baseline can retrieve several chain documents by accident.

That does not mean it has solved multi-hop reasoning.

The key limitation is that it does not use an intermediate fact from one document to formulate the next search.

## Next experiment

After observing the one-shot ranking, build a deterministic hop executor:

```text
gold hop query 1
→ retrieve document
→ expected intermediate fact

gold hop query 2
→ retrieve document
→ expected intermediate fact

...
```

This isolates retrieval-chain execution before Phase 4 introduces autonomous planning.
