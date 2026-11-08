# Phase 5 — When Chunking Cannot Reduce Context

## Important principle

Chunking only reduces downstream context if the source unit is larger than the local evidence window.

If a section is:

```text
12–15 words
```

and the selected chunk plus neighbor covers almost all of it, then:

```text
local window ≈ full section
```

No chunking policy can demonstrate meaningful context savings there.

## EXP-049

The current retained sections average:

```text
23.33 words/query
```

across two sections.

The deduplicated chunk windows also average:

```text
23.33 words/query
```

So the mechanism works, but the benchmark is too short to test the intended efficiency benefit.

## Research lesson

Do not conclude:

```text
chunk hierarchy provides no context savings
```

from this corpus.

The correct conclusion is:

```text
the current synthetic sections are too short to measure the benefit.
```

## Next benchmark requirement

Create longer sections containing:

- relevant evidence,
- unrelated local detail,
- neighboring distractor sentences.

Then compare full-section context against local deduplicated windows.
