# Phase 6 — Entity Linking Is Not Answer Retrieval

## The EXP-056 failure

Consider:

```text
Which service is maintained by the infrastructure reliability group?
```

There are two different semantic objects in this sentence:

```text
mention to resolve:
"infrastructure reliability group"

requested answer:
"service"
```

A whole-question embedding mixes both.

That can make the answer entity rank above the entity being referred to.

## Entity linking objective

Entity linking should answer:

```text
What graph node does this mention refer to?
```

It should not answer:

```text
What graph node best answers the whole question?
```

Those are different retrieval objectives.

## Mention detection vs entity linking

A complete linker contains two conceptual stages:

```text
question
→ mention detection
→ candidate entity ranking
```

EXP-057 gives the mention detector oracle output so we can test the second stage independently.

## Why isolate stages?

If mention-span ranking succeeds, we know the semantic entity model is useful once given the correct phrase.

Then later work should focus on mention extraction.

If mention-span ranking fails, improving mention extraction would not solve the real problem.
