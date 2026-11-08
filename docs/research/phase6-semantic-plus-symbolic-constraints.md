# Phase 6: Semantic Ranking with Symbolic Constraints

EXP-059 demonstrated an important architecture pattern:

```text
semantic retrieval alone
< semantic retrieval + structural constraints
```

The semantic model captures similarity.

The symbolic layer enforces compatibility.

For entity linking:

```text
mention
→ entity type
→ compatible candidate set
→ semantic ranking
→ confidence gate
```

Each stage has a different responsibility.

## Why this is better than one large similarity score

A service can be highly semantically related to the team that operates it.

Similarity alone does not encode which semantic role the mention refers to.

Type filtering removes candidates that cannot satisfy the requested role before ranking.

## Abstention remains necessary

Type compatibility does not imply factual relevance.

An unrelated question about a corporate-travel team may still match the type `team`.

The confidence gate therefore remains necessary after type filtering.
